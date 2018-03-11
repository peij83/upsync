from remote_synchronizer.model.remote_manager_base import remote_manager_base
from asq import query
from .onedrive_assembler import to_onedrive_item
from remote_synchronizer.model.remote_item import item_type
import onedrivesdk

import os

class onedrive_remote_manager(remote_manager_base):
    
    def __init__(self, remote_client):
        self._client = remote_client
        self._sync_upload_max_size = 4096
    
    def get_items(self, path):
        return query(self._client.item(drive='me', path=path).children.get())\
            .select(lambda i: to_onedrive_item(i, os.path.join(path, i.name)))

    
    def get_directories(self, path):
        return self.get_items(path)\
            .where(lambda i: i.item_type == item_type.Folder)


    def get_files(self, path):
        return self.get_items(path)\
            .where(lambda i: i.item_type == item_type.File)

    def download_item(self, remote_id, destination):
        pass

    def upload_item(self, remote_path, local_path, filename):
        local_file_size = os.stat(local_path).st_size
        
        if local_file_size > self._sync_upload_max_size:
            self._client.item(drive='me', path=remote_path).children[filename].upload_async(local_path)
        else:
            self._client.item(drive='me', path=remote_path).children[filename].upload(local_path)
        
    def delete_item(self, item):
        self._client.item(drive='me', id=item.id).delete()

    def create_directory(self, name, parent_path):
        f = onedrivesdk.Folder()
        i = onedrivesdk.Item()
        i.name = name
        i.folder = f
        self._client.item(drive='me', path=parent_path).children.add(i)