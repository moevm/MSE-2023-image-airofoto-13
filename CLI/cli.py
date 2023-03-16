from click import Argument

from CLI.cli_base import *
from CLI.commands import *
from CLI.data_transfer import Backbone, pass_backbone


class CliFactory(IFactory):
    @staticmethod
    def create():
        commands = [load, execute, setup, move, rotate, cut, patch, clear, mount]

        return Cli(commands)


class Cli(ICLI):
    def __init__(self, commands: list):

        for command in commands:
            self.set_command(command)

    @classmethod
    def create_cli(cls):
        return CliFactory.create()

    @pass_backbone
    def set_command(self, backbone: Backbone, command: Command) -> None:
        backbone.commands[command.name] = command
        self.entry_point.add_command(command, command.name)

    def generate_command(self, name: str, args: Signature) -> None:
        new_command = Command(name=name)

        for arg in args.parameters:
            new_command.params.append(Argument(arg, required=True, type=args.parameters[arg].annotation,
                                               default=args.parameters[arg].default))

        self.set_command(new_command)

    @staticmethod
    @click.group(chain=True)
    @click.pass_context
    @click.option("--dest", type=click.Path(), required=False, default="", help="to save the results to")
    def entry_point(ctx: click.Context, dest: str) -> None:
        backbone = Backbone()

        backbone.add_to_config("dest", dest)

        ctx.obj = backbone
