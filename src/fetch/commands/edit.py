
import logging

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):
    edit_cmd = subparsers.add_parser(
        'edit',
        help="edit an existing bank connection",
        parents=parents,
    )
    edit_cmd.set_defaults(func=run)

def run(args):
    logger.debug("edit")
