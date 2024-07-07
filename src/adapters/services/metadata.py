from abc import ABC
from typing import Any, Optional

from src.domain.entities.metadata import Metadata
from src.domain.ports.repositories.metadata import MetadataRepositoryInterface
from src.domain.ports.services.metadata import MetadataServiceInterface
from src.domain.schemas import CreateMetadataInputDto


class MetadataService(MetadataServiceInterface, ABC):
    def __init__(self, repository: MetadataRepositoryInterface) -> None:
        self.repository = repository

    def _create(self, metadata: CreateMetadataInputDto) -> Optional[Metadata]:
        metadata_dict = metadata.model_dump()
        self.repository.add(Metadata.from_dict(metadata_dict))

    def _get_metadata_by_uuid(self, uuid: str) -> Metadata:
        pass

    def _get_all_metadata(self) -> Optional[list[Any]]:
        pass