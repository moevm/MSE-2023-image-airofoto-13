from typing import Callable, Any
import open3d as o3d  # type: ignore
import yaml

from .parser_base import IParserFactory, read_stream, write_stream
from .parser import Parser


class ParserFactory(IParserFactory):
    @staticmethod
    def create(
        name: str, reader: Callable[[str], Any], writer: Callable[[str, Any], None]
    ) -> Parser:

        return Parser(file_format=name, reader=reader, writer=writer)

    @staticmethod
    def create_yml() -> Parser:
        """
        Returns a .yml file oriented Parser instance.

        Note: Writing method is modified with a wrapper to prevent dictionary keys from being sorted.

        :return: Parser
        """

        # typing args/kwargs in typing.Callable is weird, so for now the simpler solution is in place.
        def yml_write_wo_sorting(stream: Any, data: Any) -> None:
            """
            A function wrapper redefining the standard yaml dump function,
            preventing int from sorting dictionary keys.

            :param stream: IO stream to file.
            :param data: sequence to be dumped into .yml file.
            :return: None
            """

            yaml.safe_dump(data, stream, sort_keys=False)

        return ParserFactory.create(
            "yml", read_stream(yaml.safe_load), write_stream(yml_write_wo_sorting)
        )

    @staticmethod
    def create_ply() -> Parser:
        return ParserFactory.create(
            "ply", o3d.io.read_point_cloud, o3d.io.write_point_cloud
        )

    @staticmethod
    def create_txt() -> Parser:

        def read_txt(path: str) -> Any:
            with open(path, "r") as file:
                data = file.read()

            return data

        def write_txt(path: str, data: Any) -> None:
            with open(path, "w") as file:
                file.write(data)


        return ParserFactory.create(
            "txt", read_txt, write_txt
        )