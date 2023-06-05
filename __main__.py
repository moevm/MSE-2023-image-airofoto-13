#!/usr/bin/python

from CLI import CLIBuilder, Backbone
from managers import PluginRegistry

import open3d as o3d    # type: ignore
from inspect import Signature
from typing import Dict, Tuple


def cut_point_cloud(sig: Signature) -> Signature:

    # getting rid of the first argument of plugin functions signatures (point_cloud) is tricky,
    # since Signature objects are immutable.

    new_arguments = []

    for argument in sig.parameters:

        if sig.parameters[argument].annotation != o3d.geometry.PointCloud:
            new_arguments.append(sig.parameters[argument])

    return sig.replace(parameters=new_arguments)


def get_plugins_info() -> Dict[str, Tuple[str, Signature]]:

    reg = PluginRegistry.build()

    plugins = {name: reg.get_info(name) for name in reg.supported_plugins()}
    new_data = {}

    for name in plugins:

        new_data[name] = (
            plugins[name].desc,
            cut_point_cloud(plugins[name].sig),
        )

    return new_data


def main() -> None:

    builder = CLIBuilder()

    ui = builder.build_cli(get_plugins_info())

    config = ui.run()

    if not config:
        raise TypeError("No Backbone provided!")

    print(config.generate_config())


if __name__ == "__main__":
    main()
