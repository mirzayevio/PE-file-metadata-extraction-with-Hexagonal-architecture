from sqlalchemy import UUID, Column, DateTime, Integer, String

from src.configurator.config import Base


class MetadataModel(Base):
    __tablename__ = 'metadata'
    id = Column(UUID, primary_key=True)
    file_name = Column(String(100), nullable=False)
    file_path = Column(String(100), nullable=False)
    file_type = Column(String(10), nullable=False)  # DLL or EXE
    file_size = Column(Integer)

    architecture = Column(String(10), nullable=False)  # x32 or x64
    num_of_imports = Column(Integer)
    num_of_exports = Column(Integer)
    created = Column(DateTime)
