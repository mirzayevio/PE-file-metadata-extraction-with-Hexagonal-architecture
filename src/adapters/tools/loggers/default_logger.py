import logging
import os

from src.configurator.config import LOGS_FOLDER
from src.domain.ports.tools.loggers.logger import LoggerInterface


class LoggerDefault(LoggerInterface):
    def __init__(self):
        log_file_path = os.path.join(LOGS_FOLDER, 'app.log')
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        logging.basicConfig(
            filename=log_file_path,
            filemode='a',
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)-s - %(levelname)s - %(message)s',
            level=logging.DEBUG,
        )

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def log_debug(self, message: str) -> None:
        """
        Log debug message.
        :param message: Message to log.
        """
        logging.debug(message)

    def log_info(self, message: str) -> None:
        """
        Log info message.
        :param message: Message to log.
        """
        logging.info(message)

    def log_warning(self, message: str) -> None:
        """
        Log warning message.
        :param message: Message to log.
        """
        logging.warning(message)

    def log_error(self, message: str) -> None:
        """
        Log error message.
        :param message: Message to log.
        """
        logging.error(message)

    def log_critical(self, message: str) -> None:
        """
        Log critical message.
        :param message: Message to log.
        """
        logging.critical(message)

    def log_exception(self, message: str) -> None:
        """
        Log exception message with exception info.
        :param message: Message to log.
        """
        logging.exception(message)
