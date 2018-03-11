from .onedrive_file import onedrive_file
from .onedrive_folder import onedrive_folder

from remote_synchronizer.model.remote_item import item_type

def to_onedrive_item(item, path):
    returned_item = None
    if item.folder is None:
        returned_item = onedrive_file(item, path, item_type.File)
    else:
        returned_item = onedrive_folder(item, path, item_type.Folder)

    return returned_item
