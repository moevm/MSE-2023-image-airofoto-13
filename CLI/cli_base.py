from click import Command, Context
from inspect import Signature

from framework import *
from CLI.data_transfer import Backbone


class ICLI(ABC):

    """
    Interface for CLI class.
    Declares basic modular CLI functionality: adding and generating commands and entry point for CLI execution.
    """

    @classmethod
    @abstractmethod
    def create_cli(cls):
        """
        Factory method for easy CLI objects creation.

        :return: CLI object.
        """

        pass

    @staticmethod
    @abstractmethod
    def entry_point(ctx: Context, dest: str) -> None:

        """
        Entry point for CLI execution.

        :param ctx: Context from click library, needed for internal business logic and is passed automatically.
        :param dest: |optional| path to save result to.
        :return: None.
        """

        pass

    @abstractmethod
    def set_command(self, backbone: Backbone, command: Command) -> None:

        """
        Helper method to add command to current CLI. Invoked during CLI object initialization.

        :param backbone: business object, storing all the necessary CLI meta information,
        including the dictionary of supported commands.
        :param command: Click.Command object to add to current CLI.
        :return: None.
        """

        pass

    @abstractmethod
    def generate_command(self, name: str, args: Signature) -> None:

        """
        Creates a click.Command from given signature with a given name and adds it to the current CLI.

        :param name: name of the command.
        :param args: signature object, containing desired parameters for command.
        :return: None.
        """

        pass
