import logging
from typing import Optional

from .config import *


class Logger:
    def __init__(self, name: Optional[str] = None, level: int = 20, filename: str = "lamd.log") -> None:
        self.level = level
        self.filename = filename
        self.name = name
        format = "%(levelname)s:%(name)s:%(asctime)s:%(message)s"
        logging.basicConfig(level=level, filename=filename, format=format)
        self.logger = logging.getLogger(name)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)
