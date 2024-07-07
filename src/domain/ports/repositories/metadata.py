from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.metadata import Metadata


class MetadataRepositoryInterface(ABC):
    def add(self, metadata: Metadata) -> None:
        self._add(metadata)

    def get_by_uuid(self, uuid: str) -> Metadata:
        return self._get_by_uuid(uuid)

    def get_all(self) -> Optional[list[Metadata]]:
        return self._get_all()

    @abstractmethod
    def _add(self, metadata: Metadata) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get_by_uuid(self, uuid: str) -> Metadata:
        raise NotImplementedError

    @abstractmethod
    def _get_all(self) -> Optional[list[Metadata]]:
        raise NotImplementedError
