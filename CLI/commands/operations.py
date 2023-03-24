import click


@click.command("move", short_help="Shift points along x, y and z axes")
@click.pass_context
@click.argument("x", type=float, required=True, default=0.0)
@click.argument("y", type=float, required=True, default=0.0)
@click.argument("z", type=float, required=True, default=0.0)
def move(ctx: click.Context, x: float, y: float, z: float) -> None:
    """
    Shift all points in point cloud by given values along respective axes (X, Y and Z).

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param x: Value to shift points by along the X-axis.
    :param y: Value to shift points by along the Y-axis.
    :param z: Value to shift points by along the Z-axis.
    :return: None.
    """
    ctx.obj.enqueue("move", {"x": x, "y": y, "z": z})


@click.command("rotate", short_help="Rotate points along x, y and z axes")
@click.pass_context
@click.argument(
    "mode", type=click.Choice(["Degree", "Radian"]), required=True, default="Degree"
)
@click.argument("x", type=float, required=True, default=0.0)
@click.argument("y", type=float, required=True, default=0.0)
@click.argument("z", type=float, required=True, default=0.0)
def rotate(ctx: click.Context, mode: str, x: float, y: float, z: float) -> None:
    """
    Rotate the point cloud by given values in Degrees/Radians along respective axes (x, y and z).

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param mode: Angle units to use for rotation.
    :param x: Value to rotate points by along the X-axis.
    :param y: Value to rotate points by along the Y-axis.
    :param z: Value to rotate points by along the Z-axis.
    :return: None.
    """

    ctx.obj.enqueue("rotate", {"mode": mode, "x": x, "y": y, "z": z})


@click.command("cut", short_help="Remove points at given corners")
@click.pass_context
@click.option("--ul", is_flag=True)
@click.option("--ur", is_flag=True)
@click.option("--ll", is_flag=True)
@click.option("--lr", is_flag=True)
def cut(ctx: click.Context, ul: bool, ur: bool, ll: bool, lr: bool) -> None:
    """
    Remove points located at the corners of the point cloud.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param ul: boolean flag determining if points in the UPPER-LEFT corner should be removed.
    :param ur: boolean flag determining if points in the UPPER-RIGHT corner should be removed.
    :param ll: boolean flag determining if points in the LOWER-LEFT corner should be removed.
    :param lr: boolean flag determining if points in the LOWER-RIGHT corner should be removed.
    :return: None.
    """

    ctx.obj.enqueue(
        "cut",
        {"upper-left": ul, "upper-right": ur, "lower-left": ll, "lower-right": lr},
    )


@click.command("patch", short_help='Patch "holes" in point cloud')
@click.pass_context
@click.argument("degree", type=int, required=True, default=1)
def patch(ctx: click.Context, degree: int) -> None:
    """
    Fills empty spaces in point cloud via interpolation.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param degree: Degree of interpolation.
    :return: None.
    """

    ctx.obj.enqueue("patch", {"degree": degree})


@click.command("clear", short_help="Remove all points above\\below given height")
@click.pass_context
@click.argument("height", type=float, required=True, default=0.0)
@click.option("--above", is_flag=True)
@click.option("--below", is_flag=True)
def clear(ctx: click.Context, height: float, above: bool, below: bool) -> None:
    """
    Filter point cloud by z-axis coordinate. Removes every point above/below the given height value.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param height: z-axis value (height) to filter point cloud by.
    :param above: boolean flag to determine if points ABOVE given height should be removed.
    :param below: boolean flag to determine if points BELOW given height should be removed.
    :return: None.
    """

    ctx.obj.enqueue("clear", {"height": height, "above": above, "below": below})


@click.command("mount", short_help="Georeference given image")
@click.pass_context
@click.argument("path", type=click.Path(exists=True), default="")
def mount(ctx: click.Context, path: str) -> None:
    """
    Use the source point cloud to embed geographic information into the given (GeoTIFF) image.

    :param ctx: Context from click library, needed for internal business logic and is passed automatically.
    :param path: Path to the GeoTIFF image to embed.
    :return: None.
    """

    ctx.obj.enqueue("mount", {"path": path})
