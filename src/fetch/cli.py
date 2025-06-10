import argparse
import logging

from .commands import (
    add,
    remove,
    disable,
    edit,
    fetch,
    config,
)

def run():

    base_parser = argparse.ArgumentParser(
        prog="bf",
        description="Uses Teller API to fetch bank transactions",
        epilog=(
            "Basic usage: specify the output folder and the path to each of"
            " your Teller credentials using --cert and --cert-key flags."
        ),
    )

    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument(
        'app_id',
        help='Teller app id',
    )
    global_parser.add_argument(
        '--cert',
        type=str,
        help='path to the TLS certificate'
    )
    global_parser.add_argument(
        '--cert-key',
        type=str,
        help='path to the TLS certificate private key'
    )
    global_parser.add_argument(
        '-e',
        '--env',
        choices=["sandbox", "development", "production"],
        default="sandbox"
    )
    global_parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='enable debug logging'
    )
    subparsers = base_parser.add_subparsers(dest="command", required=True)
    for sub_cmd in [
        add,
        remove,
        disable,
        edit,
        fetch,
        config,
    ]:
        sub_cmd.add_parser(subparsers, parents=[global_parser])

    args = base_parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
    )

    args.func(args)
