+++
title = "Code highlight example"
date = "2020-03-16"
tags = []
+++

Write your article here.

```python
import pathlib
from dataclasses import dataclass
import datetime
from typing import List

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
```
