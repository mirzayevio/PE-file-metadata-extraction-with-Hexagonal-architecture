"""
This module has definition of the Metadata entity
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Metadata:
    """
    Definition of the Metadata entity
    """

    id: str
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    architecture: str
    num_of_imports: str
    num_of_exports: str
    created: datetime
