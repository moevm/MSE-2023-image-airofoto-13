from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from click import Command, Context, group, option, pass_context, Path

from CLI.commands import IConsoleCommandFactory
from CLI.data_transfer import IBackbone


class ICLI(ABC):

    @abstractmethod
    def attach_command(self, command: Command) -> None:

        """
        Adds given command to CLI instance's invokable commands.

        :param command: click.Command instance.
        :return: None.
        """

        pass

    @abstractmethod
    def attach_plugin(self, name: str, package: str) -> None:

        """
        Generates the console representation for given plugin and
        adds it to invokable commands of the current CLI instance.

        :param name: Name of the .py file containing the plugin (also the name of the target function inside the file).
        :param package: Python package, where the plugin is located.
        :return: None.
        """

        pass

    @abstractmethod
    def generate_command(self, function: Callable[[...], Any]) -> None:

        """
        Generates command from a given function and adds it to invokable commands of current CLI instance.

        :param function: Callable object.
        :return: None.
        """

        pass

    @abstractmethod
    def get_backbone(self) -> IBackbone:

        """
        Returns current CLI's DTO - IBackbone instance.

        :return: IBackbone instance.
        """

        pass

    @staticmethod
    @abstractmethod
    @group(chain=True)
    @pass_context
    @option("--path", "--p", type=Path(exists=True), help="Path to the source data .ply file.")
    @option("--dest", "--d", type=Path(exists=False), help="Path to save the program output to.")
    def entry_point(ctx: Context, path: Optional[str] = None, dest: Optional[str] = None) -> None:

        """
        Entry point for the command line interface.

        :param ctx: click.Context object. Should be passed automatically via @click.pass_context decorator.
        :param path: Path to source .ply file.
        :param dest: Path to save output file to.
        :return: None
        """

        pass


class ICLIBuilder(ABC):

    """
    Builder class for CLI.
    """

    @staticmethod
    @abstractmethod
    def get_commands() -> Dict[str, Command]:

        """
        Returns a dictionary of plugins in specified directory.

        :return: Dict with loaded plugins.
        """

        pass

    @staticmethod
    @abstractmethod
    def build_command_factory() -> IConsoleCommandFactory:

        """
        Returns a Command serialization factory for CLI.

        :return:
        """

        pass

    @staticmethod
    @abstractmethod
    def build_backbone() -> IBackbone:

        """
        Returns an IBackbone instance.

        :return: IBackbone.
        """

        pass

    @staticmethod
    @abstractmethod
    def build_cli() -> ICLI:

        """
        Creates a fully functional CLI instance.

        :return: ICLI instance.
        """

        pass
