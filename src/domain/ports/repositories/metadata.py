from abc import ABC, abstractmethod

from src.domain.entities.metadata import Metadata


class MetadataRepositoryInterface(ABC):
    def add(self, metadata: Metadata) -> None:
        self._add(metadata)

    def get_by_uuid(self, uuid: str) -> Metadata:
        return self._get_by_uuid(uuid)

    @abstractmethod
    def _add(self, metadata: Metadata) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get_by_uuid(self, uuid: str) -> Metadata:
        raise NotImplementedError
