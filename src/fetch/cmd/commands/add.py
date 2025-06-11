
import logging

from argparse import ArgumentParser
from .wrappers import *

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    add_cmd: ArgumentParser = subparsers.add_parser(
        "add",
        usage="bf add [args] [options]",
        help="Connect a new banking institution",
        parents=parents,
    )
    add_cmd.add_argument(
        "nickname",
        help=(
            "Nickname to be associated with bank connection. If none "
            "specified, a random identifier will be assigned instead."
        )
    )
    add_cmd.set_defaults(func=run)

@requires_auth
def run(args):
    logger.debug("add")
    pass
