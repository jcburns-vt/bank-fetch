import logging

from pathlib import Path

from ..common import config, keys

logger = logging.getLogger(__name__)


class CommandError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def requires_auth(func):
    def wrapper(args):
        if (
            not (cert := args.cert)
            or not (cert_key := args.cert_key)
            or not (app_id := args.app_id)
        ):
            if (
                not (cert := config.read(keys.CERT_PATH))
                or not (cert_key := config.read(keys.CERT_KEY_PATH))
                or not (app_id := config.read(keys.APP_ID))
            ):
                raise CommandError(
                    "This command requires auth. Provide your Teller "
                    "application-id, path to certificate.pem, and path to "
                    "private_key.pem via command flags or use the bf config "
                    "command to set these values permanently."
                )

        _ = app_id # appease the lsp gods

        try:
            cert_path = Path(cert)
            cert_key_path = Path(cert_key)

        except TypeError as err:
            raise CommandError(
                f"Invalid path: {err}"
            )

        if not cert_path.exists():
            raise CommandError(
                f"Specified certificate path does not exist"
            )

        if not cert_key_path.exists():
            raise CommandError(
                f"Specified private key path does not exist"
            )

        return func(args)
    return wrapper
