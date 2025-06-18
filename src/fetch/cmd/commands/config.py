
import logging

from argparse import ArgumentParser

from ..errors import CommandError
from ...app import bf_app


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
        bf_app.list_settings()
    elif (key := args.key) and (not args.value):
        bf_app.lookup_setting(key)
    elif (key := args.key) and (value := args.value):
        bf_app.edit_setting(key, value)
    else:
        raise CommandError("Specified value without a corresponding key")

