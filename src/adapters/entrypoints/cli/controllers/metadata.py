from src.domain.ports.services.metadata import MetadataServiceInterface
from src.domain.ports.services.storage import StorageServiceInterface


class MetadataController:
    def __init__(
        self,
        storage_service: StorageServiceInterface,
        metadata_service: MetadataServiceInterface,
    ):
        self.storage_service = storage_service
        self.metadata_service = metadata_service

    def execute(self, task_size: int):
        print(task_size)
        print(self.storage_service)
        print(self.metadata_service)
