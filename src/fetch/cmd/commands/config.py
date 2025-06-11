
import logging

from argparse import ArgumentParser

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    config_cmd: ArgumentParser = subparsers.add_parser(
        'config',
        help="edit persistent settings",
        parents=parents,
    )
    config_cmd.set_defaults(func=run)

def run(args):
    logger.debug("config")
