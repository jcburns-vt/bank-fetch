
import logging

from argparse import ArgumentParser

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):

    disable_cmd: ArgumentParser = subparsers.add_parser(
        "disable",
        help=(
            "Disable an existing bank connection without deleting "
            "an enrollment"
        ),
        parents=parents,
    )
    disable_cmd.set_defaults(func=run)

def run(args):
    logger.debug("disable")
