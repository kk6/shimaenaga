import pathlib
from typing import Union


def read_file(path: Union[pathlib.Path, str]) -> str:
    with open(path) as f:
        return f.read()
