from typing import Any, Callable, TypeVar

import click

from CLI.cli_base import ICLI
from CLI.commands import IConsoleCommandFactory
from CLI.data_transfer import IBackbone
from managers import PluginInfo

__all__ = ["CLI"]


BackboneReturnType = TypeVar("BackboneReturnType")


class CLI(ICLI):

    _backbone = None

    def __init__(self,
                 entry_point: click.Group,
                 command_factory: IConsoleCommandFactory,
                 backbone: IBackbone,
                 ) -> None:

        self._builder = command_factory
        self._entry_point = entry_point
        CLI._backbone = backbone

        #---------------------------------------------------------------------------------------------------------------
        # hardcoded config-utility commands

        @click.pass_context
        @click.argument("path", type=click.Path(exists=True), required=True)
        def load(ctx: click.Context, path: str) -> None:
            """
            Load config from .yml file located at the specified path.

            :param path: Path to config file.
            :return: None.
            """

            ctx.obj.load_config(path)

        @click.pass_context
        @click.argument("path", type=click.Path(exists=False), required=True)
        def dump(ctx: click.Context, path: str) -> None:
            """
            Dumps config to the specified location

            :param path: Path to save config file to.
            :return: None.
            """

            ctx.obj.dump_config(path)

        # ---------------------------------------------------------------------------------------------------------------

        self.attach_command(click.command(load))
        self.attach_command(click.command(dump))

    def attach_command(self, command: click.Command) -> None:

        self._entry_point.add_command(command, command.name)

    def attach_plugin(self, data: PluginInfo) -> None:

        self.attach_command(self._builder.create_from_info(data))

    def generate_command(self, function: Callable[[...], Any]) -> None:

        self.attach_command(self._builder.create_from_function(function))

    @staticmethod
    def get_backbone() -> IBackbone:

        return CLI._backbone

    def run(self) -> IBackbone:

        # click finishes whole execution as soon as the cli group finishes its execution.
        # The try-except block below prevents that from happening.
        try:
            self._entry_point()
        except SystemExit as error:
            if error.code:
                raise

        return self._backbone
