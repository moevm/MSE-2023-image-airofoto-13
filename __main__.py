#!/usr/bin/python

from CLI import CLIBuilder, Backbone
from mvp import Model


def main() -> None:
    ui = CLIBuilder.build_cli()

    # click finishes whole execution as soon as the cli group finishes its execution.
    # The try-except block below prevents that from happening.
    try:
        ui.entry_point()
    except SystemExit as error:
        if error.code:
            raise

    print(ui.get_backbone().generate_config())


if __name__ == "__main__":
    main()
