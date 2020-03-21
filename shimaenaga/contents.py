import pathlib
import datetime
from typing import Sequence, Type, TypeVar

import mistune
from html5lib_truncation import truncate_html
from pydantic.dataclasses import dataclass

from .parsers import parse_markdown

T = TypeVar("T", "Content", "Article")


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

    @property
    def url(self) -> pathlib.Path:
        return self.path.with_suffix(".html")


@dataclass
class Article(Content):
    path: pathlib.Path
    title: str
    date: datetime.date
    body: str
    tags: Sequence[str]

    @property
    def display_date(self) -> str:
        return self.date.strftime("%b %d, %Y")

    def summarize_html(self, length: int = 150) -> str:
        return truncate_html(self.html, length, end="...")


def load_contents(contents_dir: pathlib.Path, content_class: Type[T]) -> Sequence[T]:
    contents = []
    for path in contents_dir.glob("**/*.md"):
        content = load_content(path, content_class)
        contents.append(content)
    return contents


def load_content(path: pathlib.Path, content_class: Type[T]) -> T:
    metadata, body = parse_markdown(path)
    return content_class(path=path, body=body, **metadata)


def sort_articles(articles: Sequence[Article]) -> Sequence[Article]:
    return sorted(articles, key=lambda a: a.date, reverse=True)
