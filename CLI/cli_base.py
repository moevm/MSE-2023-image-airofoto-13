from abc import ABC, abstractmethod
from inspect import Signature
from typing import Any, Callable, Dict, Optional, Tuple

import click

from CLI.data_transfer import IBackbone
from managers import PluginInfo


class ICLI(ABC):
    @abstractmethod
    def attach_command(self, command: click.Command) -> None:

        """
        Adds given command to CLI instance's invokable commands.

        :param command: click.Command instance.
        :return: None.
        """

        pass

    @abstractmethod
    def attach_plugin(self, data: PluginInfo) -> None:

        """
        Generates the console representation for given plugin and
        adds it to invokable commands of the current CLI instance.

        :data: PluginInfo instance with information about the plugin.
        :return: None.
        """

        pass

    @abstractmethod
    def generate_command(self, function: Callable[[Any], Any]) -> None:

        """
        Generates command from a given function and adds it to invokable commands of current CLI instance.

        :param function: Callable object.
        :return: None.
        """

        pass

    @staticmethod
    @abstractmethod
    def get_backbone() -> IBackbone | None:

        """
        Returns current CLI's DTO - IBackbone instance.

        :return: IBackbone instance.
        """

        pass

    @abstractmethod
    def run(self) -> IBackbone | None:

        """
        Entry point for the command line interface.

        :return: IBackbone instance.
        """

        pass


class ICLIBuilder(ABC):

    """
    Builder class for CLI.
    """

    @abstractmethod
    def build_commands(
        self, plugins: Dict[str, Tuple[str, Signature]]
    ) -> Dict[str, click.Command]:
        """
        Generates CLI representation for plugins.

        :param plugins: Dictionary of Signature objects
        :return: Dictionary of click.Command instances
        """

        pass

    @abstractmethod
    def build_group(
        self,
        executable: Optional[Callable[[click.Context, Any], None]] = None,
        arguments: Optional[Dict[str, click.Parameter]] = None,
        chain_commands: bool = True,
    ) -> click.Group:
        """
        Creates a click.Group instance with the provided arguments and options (or the default ones),
        which serves as the entry point for CLI.

        :param executable: The function which will serve as CLI entry_point.
         Default one will be generated if None was provided.
        :param arguments: Dictionary of Parameters (Argument or Option) for entry point.
        :param chain_commands: Boolean flag to switch command chaining in click.Group instance.
        :return: click.Group instance
        """

        pass

    @abstractmethod
    def build_backbone(self) -> IBackbone:

        """
        Returns an IBackbone instance.

        :return: IBackbone.
        """

        pass

    @abstractmethod
    def build_cli(self, plugins: Dict[str, Tuple[str, Signature]]) -> ICLI:

        """
        Creates a fully functional CLI instance.

        :return: ICLI instance.
        """

        pass
