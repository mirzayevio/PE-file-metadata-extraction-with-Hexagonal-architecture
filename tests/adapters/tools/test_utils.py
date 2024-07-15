import io
from unittest.mock import patch

import pefile
import pytest

from src.adapters.tools.utils import get_metadata, is_pe_file
from src.configurator.config import Status


@pytest.fixture
def mock_logger(mocker):
    mock_logger = mocker.patch('src.adapters.tools.utils.logger')
    return mock_logger


def test_is_pe_file_is_valid():
    mock_data = (
        b'MZ'  # DOS header
        + b'\0' * 58  # 58 null bytes
        + b'\x80\0\0\0'  # PE header offset (128 in little endian)
        + b'\0' * 64  # 64 null bytes to reach offset 128
        + b'PE\0\0'  # PE signature
    )

    def mock_file(*args, **kwargs):
        return io.BytesIO(mock_data)

    with patch('builtins.open', mock_file):
        result = is_pe_file('valid.exe')
        print(f'Result: {result}')
        assert result is True


def test_is_pe_file_invalid():
    mock_data = b'MZ' + b'\x00' * 58 + b'\x80\x00\x00\x00' + b'NOPE'

    def mock_file(*args, **kwargs):
        return io.BytesIO(mock_data)

    with patch('builtins.open', mock_file):
        assert is_pe_file('invalid.exe') is False


def test_is_pe_file_no_mz_signature():
    mock_data = b'NO' + b'\x00' * 58 + b'\x80\x00\x00\x00' + b'PE\0\0'

    def mock_file(*args, **kwargs):
        return io.BytesIO(mock_data)

    with patch('builtins.open', mock_file):
        assert is_pe_file('invalid.exe') is False


def test_is_pe_file_file_not_found(mock_logger):
    with patch('builtins.open', side_effect=FileNotFoundError):
        assert is_pe_file('nonexistent.exe') is False

    mock_logger.log_exception.assert_called_once_with('File not found: nonexistent.exe')


def test_is_pe_file_permission_denied(mock_logger):
    with patch('builtins.open', side_effect=PermissionError):
        assert is_pe_file('no_permission.exe') is False
    mock_logger.log_exception.assert_called_once_with(
        'Permission denied: no_permission.exe'
    )


def test_is_pe_file_other_exception(mock_logger):
    with patch('builtins.open', side_effect=Exception('Some error')):
        assert is_pe_file('error.exe') is False
    mock_logger.log_exception.assert_called_once_with(
        'Error reading file error.exe: Some error'
    )


@pytest.fixture
def mock_pe_file():
    class MockPE:
        def __init__(self, is_dll=False, pe_type=pefile.OPTIONAL_HEADER_MAGIC_PE):
            self.is_dll = lambda: is_dll
            self.PE_TYPE = pe_type
            self.DIRECTORY_ENTRY_IMPORT = [
                type('obj', (object,), {'imports': [1, 2, 3]})
            ]
            self.DIRECTORY_ENTRY_EXPORT = type('obj', (object,), {'symbols': [1, 2]})

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def parse_data_directories(self, directories):
            pass

    return MockPE


def test_get_metadata_file_not_exist(mock_logger):
    with patch('os.path.isfile', return_value=False):
        result = get_metadata('nonexistent.exe')

        assert result['status'] == Status.FAIL.value
        assert 'file does not exist' in result['error']

    mock_logger.log_error.assert_called_once_with(
        'The file nonexistent.exe does not exist.'
    )


def test_get_metadata_not_pe_file(mock_logger):
    with patch('os.path.isfile', return_value=True), patch(
        'src.adapters.tools.utils.is_pe_file', return_value=False
    ):
        result = get_metadata('not_pe.txt')

        assert result['status'] == Status.FAIL.value
        assert "not a valid PE file (missing 'MZ' signature)." in result['error']

    mock_logger.log_error.assert_called_once_with(
        "The file not_pe.txt is not a valid PE file (missing 'MZ' signature)."
    )


def test_get_metadata_pe_format_error(mock_pe_file, mock_logger):
    with patch(
        'pefile.PE', side_effect=pefile.PEFormatError('Invalid PE format')
    ), patch('os.path.isfile', return_value=True), patch(
        'src.adapters.tools.utils.is_pe_file', return_value=True
    ):
        result = get_metadata('error.exe')

        assert result['status'] == Status.FAIL.value
        assert 'PEFormatError' in result['error']

    mock_logger.log_exception.assert_called_once_with(
        "PEFormatError in file error.exe: 'Invalid PE format'"
    )


def test_get_metadata_memory_error(mock_pe_file, mock_logger):
    with patch('pefile.PE', side_effect=MemoryError), patch(
        'os.path.isfile', return_value=True
    ), patch('src.adapters.tools.utils.is_pe_file', return_value=True):
        result = get_metadata('memory.exe')

        assert result['status'] == Status.FAIL.value
        assert 'MemoryError: File too large to process' in result['error']

    mock_logger.log_exception.assert_called_once_with(
        'MemoryError when processing file memory.exe'
    )


def test_get_metadata_unexpected_error(mock_pe_file, mock_logger):
    with patch('pefile.PE', side_effect=Exception('Unexpected error')), patch(
        'os.path.isfile', return_value=True
    ), patch('src.adapters.tools.utils.is_pe_file', return_value=True):
        result = get_metadata('error.exe')

        assert result['status'] == Status.FAIL.value
        assert 'Unexpected error: Unexpected error' in result['error']

    mock_logger.log_exception.assert_called_once_with(
        'Unexpected error processing file error.exe: Unexpected error'
    )


def test_get_metadata_success(mock_pe_file):
    with patch('pefile.PE', return_value=mock_pe_file()), patch(
        'os.path.isfile', return_value=True
    ), patch('src.adapters.tools.utils.is_pe_file', return_value=True), patch(
        'os.path.getsize', return_value=1024 * 1024
    ):
        result = get_metadata('test.exe')

        assert result['status'] == Status.SUCCESS.value
        assert result['file_type'] == 'EXE'
        assert result['architecture'] == 'x32'
        assert result['num_of_imports'] == 3
        assert result['num_of_exports'] == 2
        assert result['file_size'] == 1.0


def test_get_metadata_dll(mock_pe_file):
    with patch('pefile.PE', return_value=mock_pe_file(is_dll=True)), patch(
        'os.path.isfile', return_value=True
    ), patch('src.adapters.tools.utils.is_pe_file', return_value=True), patch(
        'os.path.getsize', return_value=1024 * 1024
    ):
        result = get_metadata('test.dll')

        assert result['file_type'] == 'DLL'


def test_get_metadata_x64(mock_pe_file):
    with patch(
        'pefile.PE',
        return_value=mock_pe_file(pe_type=pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS),
    ), patch('os.path.isfile', return_value=True), patch(
        'src.adapters.tools.utils.is_pe_file', return_value=True
    ), patch('os.path.getsize', return_value=1024 * 1024):
        result = get_metadata('test.exe')

        assert result['architecture'] == 'x64'
