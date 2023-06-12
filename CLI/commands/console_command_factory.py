from typing import Any, Callable, Dict, List
from inspect import Signature, signature

from click import Command, Parameter, Argument, pass_context, Context

from CLI.commands.console_command_base import IConsoleCommandFactory
from managers import PluginInfo


class ConsoleCommandFactory(IConsoleCommandFactory):
    def __init__(
        self, save_function: Callable[[Context, Dict[str, Any]], None]
    ) -> None:

        self._save_function = save_function

    @staticmethod
    def _get_arguments(args: Signature) -> List[Parameter]:
        argument_list: List[Parameter] = []

        for arg in args.parameters:

            if args.parameters[arg].annotation is None:
                raise ValueError(f"No type specification for {arg}!")

            argument_list.append(
                Argument(
                    [arg],
                    required=True,
                    type=args.parameters[arg].annotation,
                    # Since inspect has a special marker for non-existent default values we replace it with None
                    default=args.parameters[arg].default
                    if args.parameters[arg].default is not args.parameters[arg].empty
                    else None,
                )
            )

        return argument_list

    def kwargs_save_callback(self, name: str) -> Callable[[Context, Any], None]:
        @pass_context
        def callback(ctx: Context, **kwargs: Any) -> None:

            data: Dict[str, str | Dict[str, Any]] = {"type": name}
            data.update(**kwargs)

            self._save_function(ctx, data)

        return callback  # type: ignore

    def create_from_info(self, data: PluginInfo) -> Command:
        return self.create_from_signature(data.name, data.desc, data.sig)

    def create_from_function(self, executable: Callable[[Any], Any]) -> Command:

        return self.create_from_signature(
            name=executable.__name__,
            help_msg=str(executable.__doc__),
            arguments=signature(executable),
        )

    def create_from_signature(
        self, name: str, help_msg: str, arguments: Signature
    ) -> Command:

        return Command(
            name=name,
            params=self._get_arguments(arguments),
            callback=self.kwargs_save_callback(name),
            help=help_msg,
        )
