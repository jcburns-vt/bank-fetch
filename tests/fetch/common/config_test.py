
import pytest

from fetch.common import config
from fetch.common.config import ConfigError
from fetch.api import Enrollment

def test_get():

    config._delete_config()

    # key doesnt exist case
    with pytest.raises(ConfigError):
        config.read("buns")

    # key exists case
    config.write("hello", "wtf")
    assert config.read("hello") == "wtf"

def test_write():

    config._delete_config()

    # invalid key case

    # invalid value case

    pass

def test_save_enrollment():
    pass

def test_remove_enrollment():
    pass
