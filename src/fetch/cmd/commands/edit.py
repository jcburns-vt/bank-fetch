
import logging

from argparse import ArgumentParser

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    edit_cmd: ArgumentParser = subparsers.add_parser(
        "edit",
        help="Edit an existing bank connection",
        parents=parents,
    )
    edit_cmd.set_defaults(func=run)

def run(args):
    logger.debug("edit")
