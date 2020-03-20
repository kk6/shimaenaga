import pathlib
from dataclasses import dataclass
import datetime
from typing import List, Type

import mistune
from html5lib_truncation import truncate_html

from .parsers import parse_markdown


@dataclass
class Content:
    path: pathlib.Path
    title: str
    body: str

    @property
    def name(self) -> str:
        return self.path.name[:-3]

    @property
    def html(self) -> str:
        return mistune.html(self.body)


@dataclass
class Article(Content):
    path: pathlib.Path
    title: str
    date: str
    body: str
    tags: List[str]

    @property
    def display_date(self) -> str:
        return self.date_obj.strftime("%b %d, %Y")

    @property
    def date_obj(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.date, "%Y/%m/%d")

    def summarize_html(self, length: int = 150) -> str:
        return truncate_html(self.html, length, end="...")


def load_contents(contents_dir: pathlib.Path, content_class: Type[Content]) -> List:
    contents = []
    for path in contents_dir.glob("**/*.md"):
        content = load_content(path, content_class)
        contents.append(content)
    return contents


def load_content(path: pathlib.Path, content_class: Type[Content]) -> Content:
    metadata, body = parse_markdown(path)
    return content_class(path=path, body=body, **metadata)


def sort_articles(articles: List[Article]) -> List[Article]:
    return sorted(articles, key=lambda a: a.date_obj, reverse=True)
