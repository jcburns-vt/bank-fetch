
import logging

from argparse import ArgumentParser

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    remove_cmd: ArgumentParser = subparsers.add_parser(
        "remove",
        help="Remove an existing bank connection",
        parents=parents
    )
    remove_cmd.set_defaults(func=run)

def run(args):
    logger.debug("remove")
