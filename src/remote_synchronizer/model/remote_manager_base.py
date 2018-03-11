from abc import ABC, abstractmethod


class remote_manager_base(ABC):
    @abstractmethod
    def __init__(self, remote_client):
        pass

    @abstractmethod
    def get_items(self, path):
        pass

    @abstractmethod
    def get_directories(self, path):
        pass

    @abstractmethod
    def get_files(self, path):
        pass

    @abstractmethod
    def download_item(self, remote_id, destination):
        pass

    @abstractmethod
    def upload_item(self, path, local_path, filename):
        pass

    @abstractmethod
    def delete_item(self, remote_id):
        pass

    @abstractmethod
    def create_directory(self, name, parent_path):
        pass