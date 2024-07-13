from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    def download_files(self, count: int, download_folder: str) -> None:
        return self._download_files(count, download_folder)

    @abstractmethod
    def _download_files(self, count: int, download_folder: str) -> None:
        raise NotImplementedError
