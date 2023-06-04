#!/usr/bin/python

from CLI import CLIBuilder, Backbone
from managers import PluginRegistry

import open3d as o3d


def main() -> None:

    reg = PluginRegistry.build()

    plugins = {name: reg.get_info(name) for name in reg.supported_plugins()}

    for name in plugins:
        # getting rid of the first argument of plugin functions signatures (point_cloud) is tricky,
        # since Signature objects are immutable.
        new_parameters = []
        for arg in plugins[name].sig.parameters:

            if plugins[name].sig.parameters[arg].annotation != o3d.geometry.PointCloud:
                new_parameters.append(plugins[name].sig.parameters[arg])

        plugins[name] = (
            plugins[name].desc,
            plugins[name].sig.replace(parameters=new_parameters),
        )

    builder = CLIBuilder()

    ui = builder.build_cli(plugins)

    config = ui.run()

    print(config.generate_config())


if __name__ == "__main__":
    main()
