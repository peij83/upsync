from remote_synchronizer.model.remote_file_base import remote_file_base

class onedrive_file(remote_file_base):
    
    @property
    def id(self):
        return self._item.id

    @property
    def name(self):
        return self._item.name

    @property
    def size(self):
        return self._item.size