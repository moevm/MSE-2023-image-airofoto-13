import click
from inspect import Signature
from typing import Callable, Dict, Optional, Tuple
from click import Group, Command, Parameter, Option, Choice, Path

from CLI.cli_base import ICLI, IBackbone, ICLIBuilder
from CLI.commands import IConsoleCommandFactory, ConsoleCommandFactory
from CLI.data_transfer.backbone import Backbone, save_to_backbone
from CLI.cli import CLI


class CLIBuilder(ICLIBuilder):
    def __init__(
        self, command_factory: Optional[IConsoleCommandFactory] = None
    ) -> None:

        if not command_factory:
            command_factory = ConsoleCommandFactory(save_function=save_to_backbone)

        self._command_builder = command_factory

        self._cli_arguments = {
            "logging": Option(
                ["--log"],
                type=Choice(["no", "info", "debug"], case_sensitive=False),
                default="info",
                help="Logging mode. 'no' - silent mode with no logging at all. 'info' - basic logging."
                " 'debug' - detailed logging for debugging",
            ),
            "source_path": Option(
                ["--path", "--p"],
                type=Path(exists=True),
                help="Path to the source data .ply file.",
            ),
            "save_path": Option(
                ["--dest", "--d"],
                type=Path(exists=False),
                help="Path to save the program output to.",
            ),
        }

    def build_commands(
        self, plugins: Dict[str, Tuple[str, Signature]]
    ) -> Dict[str, Command]:

        commands = {}

        for name in plugins:
            commands[name] = self._command_builder.create_from_signature(
                name, plugins[name][0], plugins[name][1]
            )

        return commands

    def build_group(
        self,
        executable: Optional[Callable[[click.Context, ...], None]] = None,
        arguments: Optional[Dict[str, Parameter]] = None,
        chain_commands: bool = True,
    ) -> Group:

        if not executable:

            @click.group("entry_point", chain=chain_commands)
            @click.pass_context
            def standard(
                ctx: click.Context,
                log: str,
                path: Optional[str] = None,
                dest: Optional[str] = None,
            ) -> None:
                ctx.obj = CLI.get_backbone()

                # TODO implement logging settings

                ctx.obj.set_source(path)
                ctx.obj.set_destination(dest)

            executable = standard

        else:

            executable = click.Group(
                name="entry_point", callback=executable, chain=chain_commands
            )

        for parameter in self._cli_arguments:
            executable.params.append(self._cli_arguments[parameter])

        return executable

    def build_backbone(self) -> IBackbone:

        return Backbone()

    def build_cli(
        self, plugins: Optional[Dict[str, Tuple[str, Signature]]] = None
    ) -> ICLI:

        entry_point = self.build_group()

        if plugins:

            commands = self.build_commands(plugins)

            for command in commands:
                entry_point.add_command(commands[command])

        return CLI(entry_point, self._command_builder, self.build_backbone())
