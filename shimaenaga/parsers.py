import pathlib
from typing import Tuple, Dict

import mistune
import tomlkit

from .files import read_file


def parse_markdown(markdown_path: pathlib.Path) -> Tuple[Dict, str]:
    text = read_file(markdown_path)
    _, meta_text, markdown = text.split("+++\n")
    metadata = tomlkit.parse(meta_text)
    html = mistune.html(markdown)
    return metadata, html
