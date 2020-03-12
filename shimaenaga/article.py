from dataclasses import dataclass
import pathlib
from typing import List

from .parsers import parse_markdown


@dataclass
class Article:
    path: pathlib.Path
    title: str
    body: str
    tags: List[str]

    @property
    def name(self) -> str:
        return self.path.name[:-3]


def load_articles(articles_dir: pathlib.Path) -> List[Article]:
    articles = []
    for article_path in articles_dir.glob("**/*.md"):
        article = load_article(article_path)
        articles.append(article)
    return articles


def load_article(path: pathlib.Path) -> Article:
    metadata, body = parse_markdown(path)
    return Article(path, metadata["title"], body, metadata["tags"])
