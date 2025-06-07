
import json
import csv
import keyring
import argparse
import requests
import time
import webbrowser
import os
import sys
import logging

from flask import Flask, render_template, request, jsonify
from multiprocessing import Process, Event
from requests.models import HTTPError
from datetime import datetime

logger = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser(
        prog="Teller Fetch",
        description="Uses Teller API to fetch bank transactions",
        epilog=(
            "Basic usage: specify the output folder and the path to each of"
            " your Teller credentials using --cert and --cert-key flags."
        ),
    )
    parser.add_argument(
        'app_id',
        help='Teller app id',
    )
    parser.add_argument(
        'output_folder',
        help='path to desired output folder',
    )
    parser.add_argument(
        '--date-from',
        type=str,
        help="oldest desired record date in form yyyy-mm-dd",
    ),
    parser.add_argument(
        '--date-to',
        type=str,
        help="newest desired record date in form yyyy-mm-dd",
    ),
    parser.add_argument(
        '--cert',
        type=str,
        help='path to the TLS certificate'
    )
    parser.add_argument(
        '--cert-key',
        type=str,
        help='path to the TLS certificate private key'
    )
    parser.add_argument(
        '-r',
        '--reset',
        action='store_true',
        help='discard saved credentials and setup from scratch',
    )
    parser.add_argument(
        '-e',
        '--env',
        choices=["sandbox", "development", "production"],
        default="sandbox"
    )
    parser.add_argument(
        '--file-type',
        choices=["json", "csv"],
        help="output file type"
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='enable debug logging'
    )
    args = parser.parse_args()

    if (not args.cert) or (not args.cert_key):
        parser.error(
            f"Must specify the location of Teller CERT and CERT_KEY."
            f"\n\tUse flags --cert and --cert-key respectively."
        )

    if not os.path.isfile(args.cert):
        parser.error(
            f"Invalid certificate path: {args.cert}"
        )

    if not os.path.isfile(args.cert_key):
        parser.error(
            f"Invalid private key path: {args.cert_key}"
        )

    if args.date_from:
        try:
            datetime.strptime(args.date_from, "%Y-%m-%d")
        except ValueError:
            parser.error(
                f"Invalid DATE_FROM value: {args.date_from}"
            )

    if args.date_to:
        try:
            datetime.strptime(args.date_to, "%Y-%m-%d")
        except ValueError:
            parser.error(
                f"Invalid DATE_TO value: {args.date_to}"
            )

    return args


class MicroServer:
    def __init__(self, app_id, environment):
        self._app_id = app_id
        self._environment = environment
        self._app = Flask(__name__)
        self._token_received_event = Event()
        self._register_routes()

    def connect_account(self):
        flask_process = Process(target=self._app.run)
        flask_process.start()
        webbrowser.open("http://127.0.0.1:5000")
        self._token_received_event.wait()
        time.sleep(.5)
        flask_process.terminate()
        flask_process.join()

    def _register_routes(self):

        @self._app.route("/", methods=["GET"])
        def home():
            return render_template("index.html")

        @self._app.route("/complete", methods=["POST"])
        def complete():
            access_token = request.get_json().get("access_token", None)
            if access_token:
                keyring.set_password("teller-fetch", "user", access_token)
                self._token_received_event.set()
                logger.info("Access token received successfully from web UI")
                return "Access token received. You may now close this window."
            else:
                return "No access token received.", 400

        @self._app.route("/app", methods=["GET"])
        def get_app_info():
            logger.debug("App data requested from webserver")
            data = {
                "app_id": self._app_id,
                "environment": self._environment,
            }
            return jsonify(data)

        _ = get_app_info, complete, home

class Client:
    def __init__(self, cert, cert_key, access_key):
        self._cert = (cert, cert_key)
        self._auth = (access_key, '')
        self._base_url = "https://api.teller.io"

    def get_accounts(self):
        accounts_json = self.get(f"{self._base_url}/accounts")
        accounts_list = [
            Account(account, self)
            for account in accounts_json
        ]
        return accounts_list

    def get(self, url):
        response = requests.get(
            url=url,
            cert=self._cert,
            auth=self._auth,
        )
        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.error(err)
            sys.exit(2)
        return response.json()


class Account:

    def __init__(self, json, client):
        self.name = json["name"]
        self._transactions = client.get(
            url=json["links"]["transactions"]
        )

    def get_transactions(self, date_from=None, date_to=None):

        # discard outside of date range
        pruned_transactions = []
        for transaction in self._transactions:
            date = transaction["date"]
            if date_from:
                if date < date_from:
                    continue
            if date_to:
                if date > date_to:
                    continue

            # discard unwanted fields
            transaction["processing_status"] = (
                    transaction["details"]["processing_status"]
            )
            transaction.pop("links", None)
            transaction.pop("details", None)
            transaction.pop("account_id", None)
            pruned_transactions.append(transaction)

        return pruned_transactions


def dump_transactions_json(out_file_path, transactions):
    logger.debug("dumping transactions to json file")
    with open(
        f"{out_file_path}.json",
        "w",
    ) as file:
        json.dump(transactions, file, indent=2)


def dump_transactions_csv(out_file_path, transactions):
    logger.debug("dumping transactions to csv file")
    with open(
        f"{out_file_path}.csv",
        "w",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)


def main():

    args = _parse_args()
    cert = (args.cert, args.cert_key)
    out_folder = args.output_folder
    if not (os.path.isdir(out_folder)):
        os.makedirs(out_folder, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
    )

    access_key = keyring.get_password("teller-fetch", "user")
    microserver = MicroServer(
        app_id=args.app_id,
        environment=args.env if args.env else "sandbox",
    )
    if (not access_key):
        logger.debug("no access_key found, requesting new one")
        microserver.connect_account()
    elif access_key and args.reset:
        keyring.delete_password("teller-fetch", "user")
        microserver.connect_account()
        logger.debug("access_key deleted")

    access_key = keyring.get_password("teller-fetch", "user")
    if not access_key:
        logger.error("error acquiring access_key")
        sys.exit(2)
    logger.debug("successfully acquired access_key fom keyring")

    client = Client(*cert, access_key)
    accounts_list = client.get_accounts()

    for account in accounts_list:
        out_file_name = f"{account.name}_transactions"
        out_file_path = os.path.join(out_folder, out_file_name)

        transactions = account.get_transactions(
            date_from=args.date_from if args.date_from else None,
            date_to=args.date_to if args.date_to else None,
        )

        if not args.file_type or args.file_type=="json":
            dump_transactions_json(out_file_path, transactions)
        elif args.file_type=="csv":
            dump_transactions_csv(out_file_path, transactions)

if __name__ == "__main__":
    main()

