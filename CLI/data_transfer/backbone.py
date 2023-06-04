from typing import (
    Any,
    List,
    Optional,
    Dict,
    TypeVar,
)
from os.path import join

import click

from .backbone_base import IBackbone
from managers import FileManager


BackboneCallableReturnType = TypeVar("BackboneCallableReturnType")


def save_to_backbone(ctx: click.Context, data: Dict[str, Any]) -> None:
    """
    Saves data from CLI command to Backbone instance inside click.Context object.

    :raises: TypeError: if click.Context's attribute 'obj' is not of type 'Backbone'

    :param: ctx: click.Context with attribute obj set to IBackbone instance.
    :param data: Dictionary of data to store in Backbone.
    :return: None
    """

    if type(ctx.obj) != Backbone:
        raise TypeError(
            f"Context object is not an IBackbone instance! ({type(ctx.obj)})"
        )

    ctx.obj.enqueue(data)


class Backbone(IBackbone):
    def __init__(self, requirements: Optional[List[str]] = None) -> None:

        # default paths
        self.__default_config_path: str = join(".", "config", "config.yml")
        self.__default_data_path: str = join(".", "images", "model.ply")
        self.__default_output_path: str = join(".", "output.ply")

        # config requirements
        minimal_requirements = ["src", "dest", "operations"]

        self._requirements = minimal_requirements

        if requirements is not None:
            if minimal_requirements in requirements:
                self._requirements = requirements
            else:
                raise ValueError(
                    f"Custom requirements should contain the minimal ones: {minimal_requirements}"
                )

        # config body
        self._src: str = ""
        self._dest: str = ""
        self._operation_queue: List[int] = []
        self._operations: Dict[int, Dict[str, Any]] = {}

    def set_source(self, path: str) -> None:
        self._src = path

    def get_source(self) -> str:
        if self._src:
            return self._src

        return self.__default_data_path

    def set_destination(self, path: str) -> None:
        self._dest = path

    def get_destination(self) -> str:
        return self._dest

    def get_requirements(self) -> List[str]:
        return self._requirements

    def valid_config(self, config: Dict[str | int, Any]) -> bool:

        for requirement in self._requirements:
            if requirement not in config:
                return False

        return True

    def generate_config(self) -> Dict[str | int, Any]:

        config: Dict[str | int, Any] = {
            "src": self.get_source(),
            "dest": self.get_destination(),
            "operations": self._operation_queue,
        }

        for operation in self._operation_queue:
            config[operation] = self._operations[operation]

        return config

    def load_config(self, path: Optional[str] = None) -> None:

        config: Dict[str | int, Any] = {}

        if path is not None:

            if FileManager().path_exists(path):
                config = FileManager().read(path)
            else:
                # TODO: log that loading from provided location failed
                pass

        else:
            config = FileManager().read(self.__default_config_path)

        if not self.valid_config(config):
            raise ValueError(
                f"Provided configuration doesn't meet requirements: {self.get_requirements()}"
            )

        self._src = config["src"]
        self._dest = config["dest"]
        self._operation_queue = config["operations"]

        for operation in self._operation_queue:
            self._operations[operation] = config[operation]

    def dump_config(self, path: Optional[str] = None) -> None:

        config: Dict[str | int, Any] = self.generate_config()

        if path is not None:
            FileManager().write(path, config)
        else:
            FileManager().write(self.__default_config_path, config)

    def enqueue(self, operation_params: Dict[str, Any]) -> None:

        if "type" not in operation_params:
            raise KeyError(
                'operation type ("type" key) was not found among parameters!'
            )

        index: int = len(self._operation_queue) + 1

        self._operation_queue.append(index)
        self._operations[index] = operation_params
