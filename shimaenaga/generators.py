from textwrap import dedent
import pathlib

from .files import write_file


def generate_markdown_template(dir: pathlib.Path, title: str, filename: str) -> pathlib.Path:
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
