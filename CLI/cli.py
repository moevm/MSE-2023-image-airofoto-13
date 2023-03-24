from click import Argument, Command
import click
from inspect import Signature

from CLI.cli_base import ICLI
from framework import IFactory
from CLI.commands import load, execute, setup, move, rotate, cut, patch, clear, mount
from CLI.data_transfer import Backbone, pass_backbone

__all__ = ["CliFactory", "ICLI", "Cli"]


class Cli(ICLI):
    def __init__(self, commands: list[Command]):

        for command in commands:
            self.set_command(command)

    @classmethod
    def create_cli(cls) -> "Cli":
        return CliFactory.create()

    @pass_backbone
    def set_command(self, backbone: Backbone, command: Command) -> None:
        if command.name:
            backbone.commands[command.name] = command
            self.entry_point.add_command(command, command.name)
        else:
            raise KeyError("Command with empty name provided")

    def generate_command(self, name: str, args: Signature) -> None:
        new_command = Command(name=name)

        for arg in args.parameters:
            new_command.params.append(
                Argument(
                    arg,
                    required=True,
                    type=args.parameters[arg].annotation,
                    default=args.parameters[arg].default,
                )
            )

        self.set_command(new_command)

    @staticmethod
    @click.group(chain=True)
    @click.pass_context
    @click.option(
        "--dest",
        type=click.Path(),
        required=False,
        default="",
        help="to save the results to",
    )
    def entry_point(ctx: click.Context, dest: str) -> None:
        backbone = Backbone()

        backbone.add_to_config("dest", dest)

        ctx.obj = backbone


class CliFactory(IFactory):
    @staticmethod
    def create() -> Cli:
        commands = [load, execute, setup, move, rotate, cut, patch, clear, mount]

        return Cli(commands)
