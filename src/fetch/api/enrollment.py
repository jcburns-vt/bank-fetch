import keyring

from ..common import (
    config as c,
    keys,
)

class Enrollment:
    def __init__(self, nickname, **kwargs):
        self._nickname = nickname
        self._enabled = kwargs.get(keys.ENABLED, True)
        self._access_token = keyring.get_password(self._nickname, "default")
        self._accounts = self._download_accounts()

    @classmethod
    def from_dict(cls, json_dict):
        return cls(
            nickname = json_dict[keys.NICKNAME],
            enabled = json_dict[keys.ENABLED],
        )

    def to_dict(self):
        return {
            keys.NICKNAME: self._nickname,
            keys.ENABLED: self._enabled,
        }

    def save(self):
        pass

    def _download_accounts(self):
        pass



