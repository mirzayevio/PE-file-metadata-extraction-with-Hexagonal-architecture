import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.fields import Field

from src.configurator.config import Status
from src.domain.validators import FileExtensionValidator


class CreateMetadataInputDto(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    architecture: str
    num_of_imports: str
    num_of_exports: str
    status: Status
    error: str
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @validator('file_type')
    def check_file_type(cls, v: str) -> str:
        if v not in FileExtensionValidator.valid_extensions:
            raise ValueError(
                f'Extension must be one of {FileExtensionValidator.valid_extensions}'
            )
        return v


def create_metadata_factory(input_data: dict) -> CreateMetadataInputDto:
    return CreateMetadataInputDto(**input_data)
