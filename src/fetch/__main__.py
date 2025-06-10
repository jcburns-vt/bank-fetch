
import logging

from .cmd import bf

logger = logging.getLogger(__name__)

def main():

    bf.run()

if __name__ == "__main__":
    main()


"""
def dump_transactions_json(out_file_path, transactions):
    with open(
        f"{out_file_path}.json",
        "w",
    ) as file:
        json.dump(transactions, file, indent=2)


def dump_transactions_csv(out_file_path, transactions):
    with open(
        f"{out_file_path}.csv",
        "w",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)


    args = parse_args()
    cert = (args.cert, args.cert_key)
    out_folder = args.output_folder
    if not (os.path.isdir(out_folder)):
        os.makedirs(out_folder, exist_ok=True)


    access_key = keyring.get_password("bank-fetch", "default")
    microserver = MicroServer(
        app_id=args.app_id,
        environment=args.env if args.env else "sandbox",
    )
    if (not access_key):
        logger.debug("no access_key found, requesting new one")
        microserver.connect_account()
    elif access_key and args.reset:
        keyring.delete_password("bank-fetch", "default")
        microserver.connect_account()
        logger.debug("access_key deleted")

    access_key = keyring.get_password("bank-fetch", "default")
    if not access_key:
        logger.error("error acquiring access_key")
        sys.exit(2)
    logger.debug("successfully acquired access_key fom keyring")

    client = Client(*cert, access_key)
    accounts_list: list[Account] = client.get_accounts()

    for account in accounts_list:
        out_file_name = f"{account.name}_transactions"
        out_file_path = os.path.join(out_folder, out_file_name)

        transactions = account.get_transactions(
            date_from=args.date_from if args.date_from else None,
            date_to=args.date_to if args.date_to else None,
        )

        if not args.file_type or args.file_type=="json":
            logger.info(f"dumping {account.name} transactions to json file")
            dump_transactions_json(out_file_path, transactions)
        elif args.file_type=="csv":
            logger.info(f"dumping {account.name} transactions to csv file")
            dump_transactions_csv(out_file_path, transactions)
    """


