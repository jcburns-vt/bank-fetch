
import copy
import requests
import logging
import sys

from requests.models import HTTPError

logger = logging.getLogger(__name__)

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
        transactions = copy.deepcopy(self._transactions)
        for transaction in transactions:
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

