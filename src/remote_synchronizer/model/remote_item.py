from abc import ABC, abstractproperty, abstractmethod
from enum import Enum

class item_type(Enum):
    Folder=1
    File=2

class remote_item(ABC):
    
    def __init__(self, item, path, item_type):
        self._item = item
        self._item_type = item_type
        self._path = path

    @property
    def item_type(self):
        return self._item_type

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def name(self):
        pass

    @property
    def path(self):
        return self._path

    