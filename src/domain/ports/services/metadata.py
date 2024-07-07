from abc import ABC, abstractmethod
from typing import Any, Optional

from src.domain.entities.metadata import Metadata
from src.domain.ports.repositories.metadata import MetadataRepositoryInterface
from src.domain.schemas import CreateMetadataInputDto


class MetadataServiceInterface(ABC):
    @abstractmethod
    def __init__(self, repository: MetadataRepositoryInterface) -> None:
        raise NotImplementedError

    def create(self, metadata: CreateMetadataInputDto) -> Optional[Metadata]:
        return self._create(metadata)

    def get_all_metadata(self) -> Optional[list[Any]]:
        return self._get_all_metadata()

    def get_metadata_by_uuid(self, uuid: str) -> Metadata:
        return self._get_metadata_by_uuid(uuid)

    @abstractmethod
    def _create(self, metadata: CreateMetadataInputDto) -> Optional[Metadata]:
        raise NotImplementedError

    @abstractmethod
    def _get_all_metadata(self) -> Optional[list[Any]]:
        raise NotImplementedError

    @abstractmethod
    def _get_metadata_by_uuid(self, uuid: str) -> Metadata:
        raise NotImplementedError
