from abc import ABC, abstractmethod
from enum import IntEnum, unique
from typing import Optional
from os.path import join
from os import getcwd

import logging

from framework import EmbedSingleton
from managers import FileManager


@unique
class LogLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class IBaseLogger(ABC, metaclass=EmbedSingleton):

    @abstractmethod
    def log(self, level: LogLevel, msg: str, origin: Optional[str]) -> None:
        pass

    @abstractmethod
    def debug(self, origin: str, msg: str) -> None:
        pass

    @abstractmethod
    def info(self, msg: str,  origin: Optional[str] = "") -> None:
        pass

    @abstractmethod
    def warn(self, origin: str, msg: str) -> None:
        pass

    @abstractmethod
    def error(self, origin: str, msg: str) -> None:
        pass

    @abstractmethod
    def critical(self, origin: str, msg: str) -> None:
        pass

    @abstractmethod
    def get_custom(self,
                   level: LogLevel,
                   module_name: str,
                   handler: Optional[logging.Handler] = None,
                   formatter: Optional[logging.Formatter] = None
                   ) -> logging.Logger:
        pass


class BaseLogger(IBaseLogger):

    def __init__(self,
                 level: Optional[LogLevel] = None,
                 file: Optional[str] = join(".", "logs", "main_log.txt"),
                 filemode: Optional[str] = "a",
                 msg_layout: Optional[str] = ""
                 ) -> None:

        if not level:
            level = LogLevel.INFO

        if not msg_layout:
            msg_layout = '%(asctime)s | [%(levelname)s] %(filename)s : "%(message)s" | (line %(lineno)d)\n'

        try:
            FileManager().write(file, "")
        except PermissionError as error:
            logging.log(LogLevel.CRITICAL, f"[{LogLevel.CRITICAL}] {__name__} :"
                                           f" Failed to create loging directory - permission denied!")
            raise error

        self._log_file = file
        self._output_mode = filemode
        self._layout = msg_layout

        logging.basicConfig(level=level, filename=file, filemode=filemode, format=msg_layout)

    def log(self, level: LogLevel, msg: str, origin: Optional[str]) -> None:
        if origin:
            logging.log(level, f"FROM /{origin}/ : {msg}")
        else:
            logging.log(level, f" {msg}")

    def debug(self, origin: str, msg: str) -> None:
        self.log(LogLevel.DEBUG, msg, origin)

    def info(self, msg: str, origin: Optional[str] = "") -> None:
        self.log(LogLevel.INFO, msg, origin)

    def warn(self, origin: str, msg: str) -> None:
        self.log(LogLevel.WARN, msg, origin)

    def error(self, origin: str, msg: str) -> None:
        self.log(LogLevel.ERROR, msg, origin)

    def critical(self, origin: str, msg: str) -> None:
        self.log(LogLevel.CRITICAL, msg, origin)

    def get_custom(self,
                   level: LogLevel,
                   module_name: str,
                   handler: logging.Handler = None,
                   formatter: logging.Formatter = None
                   ) -> logging.Logger:

        logger = logging.getLogger(module_name)
        logger.propagate = False
        logger.setLevel(level)

        # TODO ensure that same custom logger is not instanced (with handlers added) twice

        if not handler:
            handler = logging.FileHandler(self._log_file, self._output_mode)

        if not formatter:
            formatter = logging.Formatter(self._layout)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.debug("BaseLogger", f"custom logger for {module_name} created successfully.")

        return logger
