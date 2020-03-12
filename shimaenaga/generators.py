from textwrap import dedent
import pathlib
from datetime import date
import os

from .files import write_file


def generate_markdown_template(
    dir: pathlib.Path, title: str, filename: str
) -> pathlib.Path:
    text = dedent(
        f"""\
    +++
    title = "{title}"
    +++

    Write text here.
    """
    )
    path = dir / f"{filename}.md"
    write_file(path, text)
    return path


def generate_article_template(
    project_dir: pathlib.Path, title: str, filename: str, local_time: date
) -> pathlib.Path:
    dt = local_time
    article_dir = project_dir / f"articles/{dt.year}/{dt.month:0>2}/{dt.day:0>2}"
    if not article_dir.exists():
        os.makedirs(article_dir)
    path = article_dir / f"{filename}.md"
    text = dedent(
        f"""\
    +++
    title = "{title}"
    date = "{dt.year}-{dt.month:0>2}/{dt.day:0>2}"
    tags = []
    +++

    Write your article here.
    """
    )
    write_file(path, text)
    return path
