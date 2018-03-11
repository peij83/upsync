from abc import abstractproperty
from .remote_item import remote_item

class remote_file_base(remote_item):
    
    @abstractproperty
    def size(self):
        pass