import pathlib
from typing import Tuple, Dict

import tomlkit

from .files import read_file


def parse_markdown(markdown_path: pathlib.Path) -> Tuple[Dict, str]:
    text = read_file(markdown_path)
    _, front_matter, body = text.split("+++\n")
    front_matter = tomlkit.parse(front_matter)
    return front_matter, body
