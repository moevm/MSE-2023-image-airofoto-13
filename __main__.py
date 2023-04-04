#!/usr/bin/python
from CLI import Cli, Backbone


def main() -> None:
    ui = Cli.create_cli()

    # click finishes whole execution as soon as the cli group finishes its execution.
    # The try-except block below prevents that from happening.
    try:
        ui.entry_point()
    except SystemExit as error:
        if error.code:
            raise

    # Even after CLI finished working Backbone still holds the metadata.
    storage = Backbone()
    print(storage.get_config())


if __name__ == "__main__":
    main()
