import click


@click.command(short_help="Load source data")
@click.pass_context
@click.argument("path", type=click.Path(exists=True))
def load(ctx: click.Context, path: str) -> None:
    """
    Load the point cloud from the location provided to perform operations on.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param path: path to the file, containing source point cloud.
    :return: None.
    """
    ctx.obj.add_to_config("src", path)


@click.command(short_help="Run with provided config")
@click.pass_context
@click.argument("path", type=click.Path(exists=True))
def execute(ctx: click.Context, path: str) -> None:
    """
    Run the program with parameters specified in configuration file provided by user.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param path: Path to the configuration file (.yml) provided by user.
    :return: None
    """

    ctx.obj.config_path = path
    ctx.obj.load_config()


@click.command(short_help="Create config template")
@click.pass_context
@click.option("--path", type=click.Path(), required=False, default="")
@click.argument("commands", type=str, nargs=-1)
def setup(ctx: click.Context, path: str, commands: tuple):
    """
    Create a template configuration file at given location for future execution.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param path: Path to the desired location of config file (.yml) provided by user.
    :param commands: Sequence of command names, provided by user, to generate templates for in config file.
    :return: None.
    """
    ctx.obj.config_path = path

    create_config(commands)

    ctx.obj.dump_config()


@click.pass_context
def create_config(ctx: click.Context, commands: tuple):
    """
    Internal function, which generates configuration file template.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param commands: Sequence of command names, provided by user, to generate templates for in config file.
    :return: None.
    """
    for command in commands:
        ctx.obj.enqueue_default(command)
