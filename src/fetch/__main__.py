
import json
import keyring
import argparse
import requests
import time
import webbrowser
import os

from flask import Flask, render_template, request
from multiprocessing import Process, Event

def _parse_args():
    parser = argparse.ArgumentParser(
        prog="Teller Fetch",
        description="Uses Teller API to fetch bank transactions"
    )
    parser.add_argument(
        '--date-from',
        type=str,
        help="oldest record date in form yyyy-mm-dd",
    ),
    parser.add_argument(
        '--date-to',
        type=str,
        help="newest record date in form yyyy-mm-dd",
    ),
    parser.add_argument('--cert', type=str,
            help='path to the TLS certificate')
    parser.add_argument('--cert-key', type=str,
            help='path to the TLS certificate private key')
    parser.add_argument(
        '-r',
        '--reset',
        action='store_true',
        help='discard saved credentials and setup from scratch',
    )
    parser.add_argument(
        'output_folder',
        help='path to desired output folder',
    )
    args = parser.parse_args()

    if (not args.cert) or (not args.cert_key):
        parser.error(
            f"Must specify the location of Teller CERT and CERT_KEY."
            f"\n\tUse flags --cert and --cert-key respectively."
        )

    return args

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
templates_dir = os.path.join(base_dir, "templates")
static_dir = os.path.join(base_dir, "static")
app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
token_received_event = Event()
def connect_account():
    flask_process = Process(target=app.run)
    flask_process.start()
    webbrowser.open("http://127.0.0.1:5000")
    token_received_event.wait()
    time.sleep(.5)
    flask_process.terminate()
    flask_process.join()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/complete", methods=["POST"])
def complete():
    print(request.get_json())
    access_token = request.get_json().get("access_token", None)
    if access_token:
        keyring.set_password("teller-fetch", "user", access_token)
        token_received_event.set()
        return "Access token received. You may now close this window."
    else:
        return "No access token received.", 400


def main():
    args = _parse_args()
    cert = (args.cert, args.cert_key)
    output_folder = args.output_folder

    if args.reset:
        keyring.delete_password("teller-fetch", "user")

    access_key = keyring.get_password("teller-fetch", "user")
    if (not access_key):
        connect_account()

    access_key = keyring.get_password("teller-fetch", "user")
    print(access_key)

    response = requests.get(
        url="https://api.teller.io/accounts",
        cert=cert,
        auth=(access_key, '')
    )
    response.raise_for_status()

    accounts_json = response.json()
    for value in accounts_json:

        out_file_name = f"{value["name"]}_transactions.json"
        transactions_href = value["links"]["transactions"]

        # get transactions
        response = requests.get(
            url=transactions_href,
            cert=cert,
            auth=(access_key, ''),
        )
        transactions_json = response.json()

        # discard outside of date range
        pruned_transactions = []
        for transaction in transactions_json:
            date = transaction["date"]
            if args.date_from:
                if date < args.date_from:
                    continue
            if args.date_to:
                if date > args.date_to:
                    continue
            pruned_transactions.append(transaction)

        # dump pruned transactions to file
        with open(
            os.path.join(output_folder, out_file_name),
            "w",
        ) as file:
            json.dump(pruned_transactions, file, indent=2)


if __name__ == "__main__":
    main()

