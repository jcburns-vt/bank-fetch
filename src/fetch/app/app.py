
from ..common import config as c
from .errors import ApplicationError

class BFApp:
    def __init__(self):
        pass

    def list_settings(self):
        # TODO: make output prettier
        settings_dict = c.get_editable()
        print("\nSettings:")
        print("---------")
        for key in settings_dict.keys():
            print(f"{key}: {settings_dict[key]}")
        print()

    def lookup_setting(self, key):
        # TODO: validate input
        try:
            value = c.read(key)
            print(f"\n{key}: {value}\n")
        except c.ConfigError as err:
            raise ApplicationError(err)

    def edit_setting(self, key, value):
        # TODO: validate input
        try:
            c.read(key)
            c.write(key, value)
        except c.ConfigError as err:
            raise ApplicationError(err)


