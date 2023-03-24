from typing import Any, Dict, Optional
from abc import abstractmethod, ABC

from framework import *


class IBackbone(ABC, metaclass=EmbedSingleton):

    """
    CLI backbone interface.
    Declares the bare minimum of business logic needed from a business object for command-line interface.
    Enforces the Singleton pattern on derived classes.
    """

    @abstractmethod
    def set_config(self, config: Dict[str, Any]) -> None:

        """
        Stores the given dictionary as meta-config variable inside the Backbone class
        if the given dictionary meets minimal configuration file requirements.

        :raises: ValueError : if the minimal requirements are not met.

        :param config: dictionary, to be used as config file-meta.
        :return: None.
        """

    @abstractmethod
    def add_to_config(self, key: int | str, value: Any) -> None:

        """
        Appends a key-value pair to the current meta-config dictionary variable inside Backbone class.

        :param key: name of the parameter.
        :param value: value of the parameter.
        :return: None.
        """

    @abstractmethod
    def get_from_config(self, key: str) -> Any:

        """
        Returns a value from meta-config dictionary by given key.

        :raises: ValueError : if the key is not in meta-config.

        :param key: name of the parameter.
        :return: value of the given parameter.
        """

    @abstractmethod
    def get_config(self) -> Dict[str | int, Any]:

        """
        Returns a copy of the meta-config dictionary.

        :return: meta-config dictionary.
        """

    @abstractmethod
    def enqueue(self, operation: str, parameters: Dict[str, Any]) -> None:

        """
        A standard way to save callback results of CLI commands. Accepts input only from registered commands.

        :raises: ValueError : if there is no corresponding command in the COMMANDS dictionary of Backbone class.

        :param operation: name of the invoked command.
        :param parameters: callback results of the command.
        :return: None.
        """

    @abstractmethod
    def enqueue_default(self, operation: str) -> None:

        """
        A standard way to generate configuration file template. Similarly to ENQUEUE method requires given command
        to be registered (i.e. present in the COMMANDS dictionary of Backbone class).

        :raises: ValueError : if there is no corresponding command in the COMMANDS dictionary of Backbone class.

        :param operation: name of the desired command.
        :return: None.
        """

    @abstractmethod
    def load_config(self, path: Optional[str] = None) -> None:

        """
        Loads configuration to the Backbone class from a file either along the given path,
        or at the default location if no path was provided.

        :param path: |OPTIONAL| path to the configuration file.
        :return: None.
        """

    @abstractmethod
    def dump_config(self, path: Optional[str] = None) -> None:

        """
        Saves the current meta-config dictionary from Backbone class to either given location or the default one
        if none was given.

        :param path: |OPTIONAL| path to save the configuration file to.
        :return: None.
        """
