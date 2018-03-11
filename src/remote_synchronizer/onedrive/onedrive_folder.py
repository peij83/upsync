from remote_synchronizer.model.remote_folder_base import remote_folder_base

class onedrive_folder(remote_folder_base):
    
    @property
    def id(self):
        return self._item.id

    @property
    def name(self):
        return self._item.name
