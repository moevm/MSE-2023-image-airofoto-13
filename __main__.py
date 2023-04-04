#!/usr/bin/python

from CLI import Cli, Backbone
from mvp import Model


def main() -> None:
    ui = Cli.create_cli()

    # click finishes whole execution as soon as the cli group finishes its execution.
    # The try-except block below prevents that from happening.
    try:
        ui.entry_point()
    except SystemExit as error:
        if error.code:
            raise

    Backbone().dump_config()
    Model().save_data("")


if __name__ == "__main__":
    main()
