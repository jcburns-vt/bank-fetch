
import logging

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    add_cmd = subparsers.add_parser(
        'add',
        help="connect a new banking institution",
        parents=parents,
    )
    add_cmd.set_defaults(func=run)

def run(args):
    logger.debug("add")
    pass
