from pathlib import Path
from typing import Dict

from .parsers import *
from .file_manager_base import *


class FileManager(IFileManager):

    """
    Generic file handler class.
    """

    def __init__(self, parsers: Dict[str, IParser] = None):

        """
        Constructor method for FileManager class objects.

        :param parsers: dictionary of Parser objects, determining the supported file formats.
        """

        if parsers is None:
            # TODO ensure dynamic parser loading from parser directory.
            parsers = {"yml": YmlParser.create_parser()}

        self.__modes = parsers

    @staticmethod
    def get_format(path: str) -> str:

        """
        Helper method to determine file format, given path to file.

        :param path: path to the file.
        :return: file extension (without the dot!).
        """

        return path[path.rfind('.') + 1::]

    @staticmethod
    def get_filename(path: str) -> int:

        """
        Helper method to determine the index of the beginning of file name.
        Used to split directories from the actual file, when creating missing directories along the given path.

        :param path: path to the desired file location
        :return: index of the beginning of the file name.
        """

        return path.rfind('\\') + 1

    def path_exists(self, path: str) -> bool:
        p = Path(path)

        if p.exists():
            return True

        return False

    def create_path(self, path: str) -> None:
        p = Path(path)
        p.mkdir(parents=True)

    def supported_formats(self) -> List[str]:
        return list(self.__modes.keys())

    def is_supported(self, mode: str) -> bool:
        if mode in self.__modes:
            return True

        return False

    def read(self, path: str) -> any:
        mode = FileManager.get_format(path)

        if not self.is_supported(mode):
            raise ValueError(f"{mode} file type is not supported!")

        if not self.path_exists(path):
            raise ValueError(f"The file does not exist! (Couldn't access {path})")

        return self.__modes[mode].file_input(path)

    def write(self, path: str, data: any) -> None:
        mode = FileManager.get_format(path)

        if not self.is_supported(mode):
            raise ValueError(f"{mode} file type is not supported!")

        if not self.path_exists(path[:self.get_filename(path)]):
            self.create_path(path[:self.get_filename(path)])

        self.__modes[mode].file_output(file_path=path, data=data)
