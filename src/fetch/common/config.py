import logging
import json

from platformdirs import user_config_dir
from pathlib import Path

from . import keys

logger = logging.getLogger(__name__)


APP_NAME = "bank-fetch"
CONFIG_FILE_NAME = "config.json"
CONFIG_DIR = Path(user_config_dir(APP_NAME))
CONFIG_FILE_PATH = CONFIG_DIR / CONFIG_FILE_NAME
DEFAULT_SETTINGS = {
    keys.APP_ID: None,
    keys.CERT_PATH: None,
    keys.CERT_PATH: None,
    keys.ENROLLMENTS: [],
}


class ConfigError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def default_setup():

    if CONFIG_FILE_PATH.exists():
        logger.debug("config file found")
        return

    logger.debug("no config file found, writing defaults")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    _write_config(DEFAULT_SETTINGS)


def read(key):

    config_dict = _read_config()

    if key not in config_dict.keys():
        raise ConfigError(f"setting with key \"{key}\" not found")

    return config_dict[key]


def write(key, value):

    config_dict = _read_config()
    config_dict[key] = value
    _write_config(config_dict)


def _read_config():

    if not CONFIG_FILE_PATH.exists():
        default_setup()

    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_dict = json.load(config_file)

    return config_dict


def _write_config(config_dict):

    with open(CONFIG_FILE_PATH, "w") as config_file:
        json.dump(config_dict, config_file, indent=2)


def _delete_config():
    """For testing."""
    if CONFIG_FILE_PATH.exists():
        CONFIG_FILE_PATH.unlink()

