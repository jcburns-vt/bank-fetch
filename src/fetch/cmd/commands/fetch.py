
import logging

logger = logging.getLogger(__name__)

def add_parser(subparsers, parents):

    fetch_cmd = subparsers.add_parser(
        'fetch',
        help="fetch data from accounts",
        parents=parents,
    )
    fetch_cmd.add_argument(
        '--file-type',
        choices=["json", "csv"],
        help="output file type, default is json"
    )
    fetch_cmd.add_argument(
        'output_folder',
        help='path to desired output folder',
    )
    fetch_cmd.add_argument(
        '--date-from',
        type=str,
        help="oldest desired record date in form yyyy-mm-dd",
    )
    fetch_cmd.add_argument(
        '--date-to',
        type=str,
        help="newest desired record date in form yyyy-mm-dd",
    )
    fetch_cmd.set_defaults(func=run)

def run(args):
    logger.debug("fetch")
