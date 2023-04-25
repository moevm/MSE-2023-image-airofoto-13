from typing import Optional, Any, Callable, Dict, List
from inspect import Signature, signature

from click import Command, Argument, pass_context, Context
import open3d

from .console_command_base import IConsoleCommandFactory
from framework import Loader, Limit


class ConsoleCommandFactory(IConsoleCommandFactory):

    def __init__(self, save_function: Callable[[Context, Dict[str, Any]], None]) -> None:

        self._save_function = save_function

    @staticmethod
    def _get_arguments(name: str, args: Signature) -> List[Argument]:
        argument_list = []

        for arg in args.parameters:

            if args.parameters[arg].annotation != open3d.geometry.PointCloud:

                if args.parameters[arg].annotation is None:
                    raise ValueError(f"No type specification for {arg}!")

                arg_type = None

                if Limit().has_constraints(name, arg):
                    arg_type = Limit().get_argument_constraint(name, arg)

                argument_list.append(
                    Argument(
                        [arg],
                        required=True,
                        type=args.parameters[arg].annotation if arg_type is None else arg_type,
                        # Since inspect has a special marker for non-existent default values we replace it with None
                        default=args.parameters[arg].default if args.parameters[arg].default
                                                                is not args.parameters[arg].empty else None,
                    )
                )

        return argument_list

    def get_plugin_names(self, package: Optional[str] = None) -> List[str]:
        return Loader.lookup_plugins(package)

    def kwargs_save_callback(self, name: str) -> Callable[[Context, Any], None]:

        @pass_context
        def callback(ctx: Context, **kwargs: Dict[str, Any]) -> None:

            data = {"type": name}
            data.update(**kwargs)

            self._save_function(ctx, data)

        return callback

    def create_from_plugin(self, name: str, package: Optional[str] = None) -> Command:

        return self.create_from_function(Loader.load_plugin(name, package))

    def create_from_function(self, executable: Callable[[...], Any]) -> Command:

        return self.create_from_signature(name=executable.__name__,
                                                           help_msg=executable.__doc__,
                                                           arguments=signature(executable)
        )

    def create_from_signature(self, name: str, help_msg: str, arguments: Signature) -> Command:

        return Command(name=name,
                       params=self._get_arguments(name, arguments),
                       callback=self.kwargs_save_callback(name),
                       help=help_msg
                       )
