import pathlib
from typing import Tuple, Dict
from .files import read_file

import mistune
import tomlkit


def parse_markdown(markdown_path: pathlib.Path) -> Tuple[Dict, str]:
    text = read_file(markdown_path)
    _, meta_text, markdown = text.split("+++\n")
    metadata = tomlkit.parse(meta_text)
    html = mistune.html(markdown)
    return metadata, html
