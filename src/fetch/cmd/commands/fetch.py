
import logging

from argparse import ArgumentParser

from .wrappers import *

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):

    fetch_cmd: ArgumentParser = subparsers.add_parser(
        "fetch",
        help="Fetch data from accounts",
        parents=parents,
    )
    fetch_cmd.add_argument(
        "output_folder",
        help='Path to desired output folder',
    )
    fetch_cmd.add_argument(
        "--file-type",
        choices=["json", "csv"],
        help="Output file type, default is json"
    )
    fetch_cmd.add_argument(
        "--date-from",
        type=str,
        help="Oldest desired record date in form yyyy-mm-dd",
    )
    fetch_cmd.add_argument(
        "--date-to",
        type=str,
        help="Newest desired record date in form yyyy-mm-dd",
    )
    fetch_cmd.set_defaults(func=run)

@requires_auth
def run(args):
    logger.debug("fetch")
