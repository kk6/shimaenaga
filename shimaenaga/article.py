import pathlib
from dataclasses import dataclass
import datetime
from typing import List

import mistune
from html5lib_truncation import truncate_html

from .parsers import parse_markdown


@dataclass
class Article:
    path: pathlib.Path
    title: str
    date: datetime.date
    body: str
    tags: List[str]

    @property
    def name(self) -> str:
        return self.path.name[:-3]

    @property
    def display_date(self) -> str:
        return self.date.strftime("%b %d, %Y")

    @property
    def html(self) -> str:
        return mistune.html(self.body)

    def summarize_html(self, length: int = 150) -> str:
        return truncate_html(self.html, length, end="...")


def load_articles(articles_dir: pathlib.Path) -> List[Article]:
    articles = []
    for article_path in articles_dir.glob("**/*.md"):
        article = load_article(article_path)
        articles.append(article)
    return sorted(articles, key=lambda a: a.date, reverse=True)


def load_article(path: pathlib.Path) -> Article:
    metadata, body = parse_markdown(path)
    return Article(
        path,
        metadata["title"],
        datetime.datetime.strptime(metadata["date"], "%Y/%m/%d"),
        body,
        metadata["tags"],
    )
