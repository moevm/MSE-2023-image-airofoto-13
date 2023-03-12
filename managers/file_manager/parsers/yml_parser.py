from .parser_base import *
import yaml


class YmlParserFactory(IFactory):

    """
    Factory class for the .yml files Parser objects.
    """

    @staticmethod
    def create():

        """
        Standard method to create .yml files Parser objects.

        :return: YmlParser object.
        """

        return YmlParser(file_format="yml", reader=yaml.safe_load, writer=yaml.safe_dump)


class YmlParser(IParser):

    """
    Parser class to handle .yml files.
    """

    def __init__(self, file_format: str, reader: callable, writer: callable):

        """
        Constructor method for YmlParser class.

        :param file_format: supported file format name.
        :param reader: function, providing data extraction from file.
        :param writer: function, providing data output to the file.
        """

        self.__file_format = file_format
        self.__reader = reader
        self.__writer = writer

    @classmethod
    def create_parser(cls):
        return YmlParserFactory.create()

    def supported_format(self) -> str:
        return self.__file_format

    def file_input(self, file_path: str):

        with open(file_path, "r") as source:
            data = self.__reader(source)

        return data

    def file_output(self, file_path: str, data: any) -> None:

        with open(file_path, "w+") as dest:
            self.__writer(data=data, stream=dest, sort_keys=False)
