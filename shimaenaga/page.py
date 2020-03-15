import pathlib
from dataclasses import dataclass
from typing import List

from .parsers import parse_markdown


@dataclass
class Page:
    path: pathlib.Path
    title: str
    body: str

    @property
    def name(self) -> str:
        return self.path.name[:-3]


def load_pages(pages_dir: pathlib.Path) -> List[Page]:
    pages = []
    for page_path in pages_dir.glob("**/*.md"):
        page = load_page(page_path)
        pages.append(page)
    return pages


def load_page(path: pathlib.Path) -> Page:
    metadata, body = parse_markdown(path)
    return Page(path, metadata["title"], body)
