import onedrivesdk
import os

from asq import query

class synchronizer(object):

    def __init__(self, remote_manager, local_sync_path, remote_sync_path):
        
        self._remote_manager = remote_manager
        self._local_sync_path = local_sync_path
        self._remote_sync_path = remote_sync_path
        
    def Synchronize(self):
        self._sync_folder('')

    def _sync_folder(self, subdir):
        
        print("**************************************")
        print("Sync folder :", subdir)

        remote_dir_list = None
        remote_file_list = None
        local_dir_list = None
        local_file_list = None

        local_path = os.path.join(self._local_sync_path, subdir)
        local_items = os.listdir(local_path)

        remote_path = os.path.join(self._remote_sync_path, subdir)

        local_dir_list = query(local_items).where(lambda local_item: os.path.isdir(os.path.join(local_path, local_item))).to_list()
        local_file_list = query(local_items).where(lambda local_item: not os.path.isdir(os.path.join(local_path, local_item))).to_list()

        remote_dir_list = self._remote_manager.get_directories(remote_path).to_list()
        remote_file_list = self._remote_manager.get_files(remote_path).to_list()

        for folder in remote_dir_list:
            print("------------------------------------")
            print("Managing remote folder : ", folder.name)
            if query(local_dir_list).any(lambda local_folder: local_folder == folder.name):
                print("Will sync folder : ", folder.name)
                self._sync_folder(os.path.join(subdir,folder.name))
            else:
                print("Will delete folder : ", folder.name)
                self._remote_manager.delete_item(folder)

        folder = None

        for folder in local_dir_list:
            print("------------------------------------")
            print("Managing local folder : ", folder)
            if not query(remote_dir_list).any(lambda remote_dir: remote_dir.name == folder):
                print("Will create remote folder : ", folder)
                self._remote_manager.create_directory(folder, remote_path)
                print("Will sync folder : ", folder)
                self._sync_folder(os.path.join(subdir,folder))
        
        for remote_file in remote_file_list:
            print("------------------------------------")
            print("Managing remote file : ", remote_file.name)
            if not query(local_file_list).any(lambda local_file: local_file == remote_file.name):
                print("Will delete file : ", remote_file.name)
                self._remote_manager.delete_item(remote_file)
        
        for local_file in local_file_list:
            print("------------------------------------")
            print("Managing local file : ", local_file)
            fullname = os.path.join(local_path, local_file)
            remote_file = query(remote_file_list).first_or_default(None, lambda r: r.name == local_file)

            if remote_file is None or remote_file.size != os.stat(fullname).st_size:
                print("Will upload file : ", local_file)
                self._remote_manager.upload_item(remote_path, fullname, local_file)


    