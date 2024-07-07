from datetime import datetime

import pytest

from src.domain.entities.metadata import Metadata


@pytest.fixture()
def metadata_dict():
    return {
        'id': '123',
        'file_name': 'test_file.exe',
        'file_path': '/path/to/test_file.exe',
        'file_type': 'exe',
        'file_size': 1024,
        'architecture': 'x32',
        'num_of_imports': '10',
        'num_of_exports': '5',
        'created': '2024-07-07T12:00:00',
    }


def test_metadata_create_with_valid_parameters():
    """Tests that a Metadata object can be created with valid parameters."""
    metadata = Metadata(
        id='123',
        file_name='test_file.exe',
        file_path='/path/to/test_file.exe',
        file_type='exe',
        file_size=1024,
        architecture='x32',
        num_of_imports='10',
        num_of_exports='5',
        created=datetime(2024, 7, 7, 12, 0, 0),
    )
    assert isinstance(metadata, Metadata)


def test_metadata_with_valid_parameters(metadata_dict):
    """Tests that a Metadata object key-values are valid"""
    metadata = Metadata.from_dict(metadata_dict)

    assert metadata.id == '123'
    assert metadata.file_name == 'test_file.exe'
    assert metadata.file_path == '/path/to/test_file.exe'
    assert metadata.file_type == 'exe'
    assert metadata.file_size == 1024
    assert metadata.architecture == 'x32'
    assert metadata.num_of_imports == '10'
    assert metadata.num_of_exports == '5'
    assert metadata.created == datetime(2024, 7, 7, 12, 0, 0)
    assert isinstance(metadata.created, datetime)


def test_metadata_from_dict_invalid_date(metadata_dict):
    """Tests that invalid date format will raise ValueError"""
    invalid_metadata_dict = metadata_dict.copy()
    invalid_metadata_dict['created'] = 'invalid-date-format'

    with pytest.raises(ValueError, match='Invalid isoformat string'):
        Metadata.from_dict(invalid_metadata_dict)


def test_metadata_from_dict_missing_fields(metadata_dict):
    """Tests that missing argument will raise TypeError"""
    incomplete_metadata_dict = metadata_dict.copy()
    incomplete_metadata_dict.pop('num_of_exports')

    with pytest.raises(TypeError, match='missing 1 required positional argument'):
        Metadata.from_dict(incomplete_metadata_dict)


# Run the tests
if __name__ == '__main__':
    pytest.main()
