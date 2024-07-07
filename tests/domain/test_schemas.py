import datetime
from uuid import UUID, uuid4

import pytest

from src.domain.schemas import create_metadata_factory


@pytest.fixture()
def valid_input_data():
    return {
        'id': uuid4(),
        'file_name': 'test_file.exe',
        'file_path': '/path/to/test_file.exe',
        'file_type': 'exe',
        'file_size': 1024,
        'architecture': 'x32',
        'num_of_imports': '10',
        'num_of_exports': '5',
        'created': datetime.datetime(2024, 7, 7, 12, 0, 0),
    }


def test_create_metadata_input_dto_with_valid_data(valid_input_data):
    """Tests that create_metadata_factory can create CreateMetadataInputDto with valid data."""

    metadata_input = create_metadata_factory(valid_input_data)

    assert metadata_input.file_name == 'test_file.exe'
    assert metadata_input.file_path == '/path/to/test_file.exe'
    assert metadata_input.file_type == 'exe'
    assert metadata_input.file_size == 1024
    assert metadata_input.architecture == 'x32'
    assert metadata_input.num_of_imports == '10'
    assert metadata_input.num_of_exports == '5'
    assert isinstance(metadata_input.id, UUID)
    assert isinstance(metadata_input.created, datetime.datetime)


def test_create_metadata_input_dto_with_invalid_file_type(valid_input_data):
    """Tests that create_metadata_factory will raise ValueError if file_type is incorrect."""

    invalid_input_data = valid_input_data.copy()
    invalid_input_data['file_type'] = 'invalid_extension'

    with pytest.raises(ValueError, match='Extension must be one of'):
        create_metadata_factory(invalid_input_data)


def test_create_metadata_input_dto_with_missing_optional_fields():
    """Tests that create_metadata_factory can create CreateMetadataInputDto without optional fields."""

    input_data = {
        'file_name': 'test_file.exe',
        'file_path': '/path/to/test_file.exe',
        'file_type': 'exe',
        'file_size': 1024,
        'architecture': 'x32',
        'num_of_imports': '10',
        'num_of_exports': '5',
    }
    metadata_input = create_metadata_factory(input_data)

    assert metadata_input.file_name == 'test_file.exe'
    assert metadata_input.file_path == '/path/to/test_file.exe'
    assert metadata_input.file_type == 'exe'
    assert metadata_input.file_size == 1024
    assert metadata_input.architecture == 'x32'
    assert metadata_input.num_of_imports == '10'
    assert metadata_input.num_of_exports == '5'
    assert isinstance(metadata_input.id, UUID)
    assert isinstance(metadata_input.created, datetime.datetime)


def test_create_metadata_input_dto_default_id_and_created(valid_input_data):
    """Tests that create_metadata_factory can create CreateMetadataInputDto with optional fields."""

    metadata_input = create_metadata_factory(valid_input_data)

    assert metadata_input.id is not None
    assert isinstance(metadata_input.id, UUID)
    assert metadata_input.created is not None
    assert isinstance(metadata_input.created, datetime.datetime)


if __name__ == '__main__':
    pytest.main()
