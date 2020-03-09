from textwrap import dedent
import pathlib


def generate_template(dir: pathlib.Path, title: str, filename: str) -> str:
    text = dedent(f"""\
    +++
    title = "{title}"
    +++

    Write text here.
    """)
    path = dir / f"{filename}.md"
    with open(path, "w") as f:
        f.write(text)
    return path
