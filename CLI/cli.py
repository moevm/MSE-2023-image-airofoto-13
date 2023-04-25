from typing import Any, Dict, Callable, Optional, TypeVar

import click

from CLI.cli_base import ICLI
from .commands import IConsoleCommandFactory
from CLI.data_transfer import IBackbone

__all__ = ["CLI"]


BackboneReturnType = TypeVar("BackboneReturnType")


class CLI(ICLI):

    _backbone = None

    def __init__(self,
                 commands: Dict[str, click.Command],
                 command_factory: IConsoleCommandFactory,
                 backbone: IBackbone
                 ) -> None:

        self._commands = {}
        self._builder = command_factory
        CLI._backbone = backbone

        for command in commands:
            self.attach_command(commands[command])

    def attach_command(self, command: click.Command) -> None:
        self.entry_point.add_command(command, command.name)
        self._commands[command.name] = command

    def attach_plugin(self, name: str, package: str) -> None:

        self.attach_command(self._builder.create_from_plugin(name, package))

    def generate_command(self, function: Callable[[...], Any]) -> None:

        self.attach_command(self._builder.create_from_function(function))

    def get_backbone(self) -> IBackbone:

        return CLI._backbone

    @staticmethod
    @click.group(chain=True)
    @click.pass_context
    @click.option("--path", "--p", type=click.Path(exists=True), help="Path to the source data .ply file.")
    @click.option("--dest", "--d" , type=click.Path(), help="Path to save the program output to.")
    def entry_point(ctx: click.Context, path: Optional[str] = None, dest: Optional[str] = None) -> None:

        ctx.obj = CLI._backbone

        ctx.obj.set_source(path)
        ctx.obj.set_destination(dest)


@CLI.entry_point.command()
@click.pass_context
@click.argument("path", type=click.Path(exists=True), required=True)
def load(ctx: click.Context, path: str) -> None:

    """
    Load config from .yml file located at the specified path.

    :param path: Path to config file.
    :return: None.
    """

    ctx.obj.load_config(path)

@CLI.entry_point.command()
@click.pass_context
@click.argument("path", type=click.Path(exists=False), required=True)
def dump(ctx: click.Context, path: str) -> None:

    """
    Dumps config to the specified location

    :param path: Path to save config file to.
    :return: None.
    """

    ctx.obj.dump_config(path)
