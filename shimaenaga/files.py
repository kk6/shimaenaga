import pathlib
from typing import Union


def read_file(path: Union[pathlib.Path, str]) -> str:
    with open(path) as f:
        return f.read()


def write_file(path: Union[pathlib.Path, str], text: str) -> None:
    with open(path, "w") as f:
        f.write(text)
