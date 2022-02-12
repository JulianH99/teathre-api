

from msilib.schema import Error
from typing import Any


class Globals:

    _globs = {}

    @classmethod
    def set(cls, attr_name: str, value: Any):
        cls._globs[attr_name] = value

    @classmethod
    def get(cls, attr_name: str):
        if attr_name not in cls._globs:
            raise Error(f"{attr_name} not found in globals")
        return cls._globs[attr_name]
