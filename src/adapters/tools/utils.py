import os

import pefile

from src.adapters.tools.loggers.spark_logger import LoggerSpark
from src.configurator.config import SPARK_LOGS, Status

logger = LoggerSpark(SPARK_LOGS)


def get_metadata(file_path: str):
    """
    Extract metadata from a PE file.

    :param file_path:
    :return dict[str, Any]: Metadata of the file.
    """
    result = {
        'file_path': file_path,
        'file_type': None,
        'file_size': 0.0,
        'architecture': None,
        'num_of_imports': 0,
        'num_of_exports': 0,
        'status': Status.FAIL.value,
        'error': None,
    }
    if not os.path.isfile(file_path):
        logger.log_error(f'The file {file_path} does not exist.')
        result['error'] = 'file does not exist.'
        return result

    if not is_pe_file(file_path):
        logger.log_error(
            f"The file {file_path} is not a valid PE file (missing 'MZ' signature)."
        )
        result['error'] = "not a valid PE file (missing 'MZ' signature)."
        return result

    try:
        with pefile.PE(file_path, fast_load=True) as pe:
            pe.parse_data_directories(
                directories=[
                    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
                    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
                ]
            )

            file_size_bytes = os.path.getsize(file_path)
            file_size = file_size_bytes / (1024 * 1024)
            file_type = 'DLL' if pe.is_dll() else 'EXE'
            architecture = (
                'x64' if pe.PE_TYPE == pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS else 'x32'
            )

            import_count = (
                sum(len(entry.imports) for entry in pe.DIRECTORY_ENTRY_IMPORT)
                if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT')
                else 0
            )

            export_count = (
                len(pe.DIRECTORY_ENTRY_EXPORT.symbols)
                if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT')
                else 0
            )

            result.update(
                {
                    'file_path': file_path,
                    'file_type': file_type,
                    'file_size': file_size,
                    'architecture': architecture,
                    'num_of_imports': import_count,
                    'num_of_exports': export_count,
                    'status': Status.SUCCESS.value,
                    'error': '',
                }
            )

    except pefile.PEFormatError as e:
        logger.log_exception(f'PEFormatError in file {file_path}: {e}')
        result['error'] = f'pefile.PEFormatError {e}'
    except MemoryError:
        logger.log_exception(f'MemoryError when processing file {file_path}')
        result['error'] = 'MemoryError: File too large to process'
    except Exception as e:
        logger.log_exception(f'Unexpected error processing file {file_path}: {e}')
        result['error'] = f'Unexpected error: {e}'

    return result


def is_pe_file(file_path: str) -> bool:
    """
    Checks if a given file is a Portable Executable (PE) file.

    This function first checks if the file starts with the 'MZ' signature,
    indicative of an MS-DOS executable. Then, it reads the offset to the
    PE header and checks for the 'PE\\0\\0' signature to confirm the file
    is a PE file.

    :param file_path:
    :return: bool True if the file is a PE file, False otherwise.
    """
    try:
        with open(file_path, 'rb') as f:
            magic = f.read(2)
            if magic != b'MZ':
                return False
            f.seek(60)  # PE header offset is at 0x3C (60 in decimal)
            pe_offset = int.from_bytes(f.read(4), 'little')
            f.seek(pe_offset)
            pe_header = f.read(4)
            return pe_header == b'PE\0\0'
    except FileNotFoundError:
        logger.log_exception(f'File not found: {file_path}')
        return False
    except PermissionError:
        logger.log_exception(f'Permission denied: {file_path}')
        return False
    except Exception as e:
        logger.log_exception(f'Error reading file {file_path}: {e}')
        return False
