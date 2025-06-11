
import logging

from argparse import ArgumentParser

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    list_cmd: ArgumentParser = subparsers.add_parser(
        "list",
        help="List existing bank connections",
        parents=parents
    )
    list_cmd.set_defaults(func=run)

def run(args):
    logger.debug("list")
