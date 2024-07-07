from sqlalchemy import Column, Integer, String

from src.configurator.config import Base


class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True)
    file_path = Column(String(100), nullable=False)
    file_type = Column(String(10), nullable=False)  # DLL or EXE
    file_size = Column(Integer)

    architecture = Column(String(10), nullable=False)  # x32 or x64
    num_of_imports = Column(Integer)
    num_of_exports = Column(Integer)
