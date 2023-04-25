from .cli_base import ICLI, IBackbone, ICLIBuilder
from .commands import IConsoleCommandFactory, ConsoleCommandFactory
from .data_transfer.backbone import Backbone, save_to_backbone
from .cli import CLI

from typing import Dict

from click import Command
from os.path import join


class CLIBuilder(ICLIBuilder):

    __plugins_path = join(".", "plugins")

    @staticmethod
    def get_commands() -> Dict[str, Command]:

        factory: IConsoleCommandFactory = CLIBuilder.build_command_factory()

        names = factory.get_plugin_names(CLIBuilder.__plugins_path)
        plugins: Dict[str, Command] = {}

        for name in names:

            plugins[name] = factory.create_from_plugin(name)

        return plugins

    @staticmethod
    def build_command_factory() -> IConsoleCommandFactory:

        return ConsoleCommandFactory(save_function=save_to_backbone)

    @staticmethod
    def build_backbone() -> IBackbone:

        return Backbone()

    @staticmethod
    def build_cli() -> ICLI:

        return CLI(CLIBuilder.get_commands(),
                   CLIBuilder.build_command_factory(),
                   CLIBuilder.build_backbone())
