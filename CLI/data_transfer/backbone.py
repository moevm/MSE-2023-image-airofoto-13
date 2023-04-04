from typing import (
    Any,
    List,
    Callable,
    Optional,
    Dict,
    TypeVar,
)
from functools import wraps
from os.path import join

from managers import FileManager
from mvp import Model
from .backbone_base import *
from click import Command


BackboneCallableReturnType = TypeVar("BackboneCallableReturnType")


class Backbone(IBackbone):

    """
    Business object class to store and process CLI data. Main objectives: configuration file handling and cli-command
    meta-data storage.

    Utilizes Singleton pattern, so there can only be one instance of Backbone class at any time.
    """

    def __init__(self, requirements: Optional[List[str]] = None):

        """
        Constructor method for Backbone class.

        Due to Singleton pattern architecture acts as a global access point. In other words the class object is
        being initialized only the first time this method is called.

        :param requirements: Configuration file requirements to enforce.
        """

        if not requirements:
            requirements = Backbone.get_minimal_requirements()

        if not Backbone.check_keys(requirements):
            raise ValueError(
                f"Minimal requirements are not met! {Backbone.get_minimal_requirements()} are needed."
            )

        self.__config: Dict[str | int, Any] = dict.fromkeys(requirements)
        self.__config["src"] = join(".", "images", "model.ply")
        self.__config["dest"] = ""
        self.__config["operations"] = [1]
        self.__config[1] = {
            "type": "rotate",
            "mode": "Degree",
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
        }

        self.__default_config_path = join(".", "config", "config.yml")
        self.config_path = ""

        self.commands: dict[str, Command] = {}

        self.__file = FileManager()

    @staticmethod
    def get_minimal_requirements() -> List[str]:

        """
        Hardcoded minimal requirements for configuration file.

        :return: List of string keys for the __config dictionary.
        """

        return ["src", "dest", "operations"]

    @staticmethod
    def check_keys(keys: List[str]) -> bool:

        """
        Method enforcing the minimal requirements for configuration file.

        :param keys: parameters to be checked.
        :return: boolean check result.
        """

        minimal_requirements = Backbone.get_minimal_requirements()

        for requirement in minimal_requirements:
            if requirement not in keys:
                return False

        return True

    def get_config_path(self) -> str:

        """
        Helper method to handle configuration file pathfinding.

        :return: Either user-provided path or the hardcoded default one.
        """

        if not self.config_path:
            return self.__default_config_path

        return self.config_path

    def add_to_config(self, key: int | str, value: Any) -> None:
        self.__config[key] = value

    def get_from_config(self, key: str) -> Any:
        if key not in self.__config:
            raise ValueError(f"{key} not found in config!")

    def enqueue(self, operation: str, parameters: Dict[str, Any]) -> None:

        if operation not in self.commands:
            raise ValueError(f"{operation} is not supported!")

        insert = {"type": operation}
        insert.update(parameters)

        number = len(self.__config["operations"]) + 1

        self.__config["operations"].append(number)

        self.add_to_config(number, insert)

        Model().task(operation, FileManager().read(self.__config["src"]), **parameters)

    def enqueue_default(self, operation: str) -> None:

        if operation not in self.commands:
            raise ValueError(f"{operation} is not supported!")

        params: dict[str, Any] = {"type": operation}

        for arg in self.commands[operation].params:
            if arg.name:
                params[arg.name] = arg.default
            else:
                raise KeyError("No argument name provided")

        number = len(self.__config["operations"]) + 1

        self.__config["operations"].append(number)

        self.add_to_config(number, params)

    def set_config(self, config: Dict[str, Any]) -> None:
        if not Backbone.check_keys(list(config.keys())):
            raise ValueError(
                f"Minimal requirements are not met! {Backbone.get_minimal_requirements()} are needed."
            )

        self.__config["src"] = config["src"]
        self.__config["dest"] = config["dest"]

        self.__config["operations"] = config["operations"]

        for operation in self.__config["operations"]:
            self.__config[operation] = config[operation]

    def get_config(self) -> Dict[str | int, Any]:
        return self.__config

    def load_config(self, path: Optional[str] = None) -> None:
        if not path:
            path = self.get_config_path()

        configuration = self.__file.read(path)

        self.set_config(configuration)

    def dump_config(self, path: Optional[str] = None) -> None:
        if not path:
            path = self.get_config_path()

        self.__file.write(path=path, data=self.__config)


# TODO сделать более универсальную анннотацию после стабилизации поддержки TypeVarTuple и TypeVarDict
def pass_backbone(
    f: Callable[[Any, Backbone, Any], BackboneCallableReturnType]
) -> Callable[..., BackboneCallableReturnType]:

    """
    Decorator to pass Backbone object to a given function. Similar to Click's pass_context,
    but does not raise error if Backbone is not initialized.

    :param f: function to wrap.
    :return: wrapped function.
    """

    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:

        new_args = list(args)
        new_args.insert(1, Backbone())
        args = tuple(new_args)

        return f(*args, **kwargs)

    return decorated
