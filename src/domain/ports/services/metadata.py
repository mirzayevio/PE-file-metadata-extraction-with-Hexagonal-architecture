from abc import ABC, abstractmethod

from src.domain.ports.repositories.metadata import MetadataRepositoryInterface


class MetadataServiceInterface(ABC):
    @abstractmethod
    def __init__(self, repository: MetadataRepositoryInterface) -> None:
        raise NotImplementedError

    def create(self, metadata):
        return self._create(metadata)

    def get_metadata_by_uuid(self, uuid: str):
        return self._get_metadata_by_uuid(uuid)

    @abstractmethod
    def _create(self, metadata):
        raise NotImplementedError

    @abstractmethod
    def _get_metadata_by_uuid(self, uuid: str):
        raise NotImplementedError
