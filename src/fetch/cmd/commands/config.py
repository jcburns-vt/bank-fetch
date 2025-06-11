
import logging

from argparse import ArgumentParser

from ..errors import CommandError

from ...common import config as c

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    config_cmd: ArgumentParser = subparsers.add_parser(
        "config",
        usage="bf config [setting_key] [value]",
        help=(
            "Edit persistent settings.\nUse config command without any "
            "arguments to view all editable settings.\nSpecifying only the "
            "setting key yields the value associated with that key."
        ),
        parents=parents,
    )
    config_cmd.add_argument(
        "key",
        nargs="?",
        help="The name of the setting to be changed",
    )
    config_cmd.add_argument(
        "value",
        nargs="?",
        help="The value to change the specified setting to",
    )
    config_cmd.set_defaults(func=run)

def run(args):
    logger.debug("config")

    if (not args.key) and (not args.value):
        list_settings()
    elif (key := args.key) and (not args.value):
        lookup_setting(key)
    elif (key := args.key) and (value := args.value):
        edit_setting(key, value)
    else:
        raise CommandError("Specified value without a corresponding key")


def list_settings():
    # TODO: make output prettier
    settings_dict = c.get_editable()
    print("\nSettings:")
    print("---------")
    for key in settings_dict.keys():
        print(f"{key}: {settings_dict[key]}")
    print()


def lookup_setting(key):
    # TODO: validate input
    try:
        value = c.read(key)
        print(f"\n{key}: {value}\n")
    except c.ConfigError as err:
        raise CommandError(err)


def edit_setting(key, value):
    # TODO: validate input
    try:
        c.read(key)
        c.write(key, value)
    except c.ConfigError as err:
        raise CommandError(err)



