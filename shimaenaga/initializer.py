import os
from textwrap import dedent

from .config import create_config_file, Config


def initialize(config: Config) -> None:
    create_config_file(config)
    create_directories()
    create_example_page()


def create_directories() -> None:
    for dirname in ("pages", "articles"):
        if not os.path.exists(dirname):
            os.mkdir(dirname)


def create_example_page() -> None:
    s = dedent(
        """\
        +++
        title = "Example"
        +++

        This is example page.
        """
    )
    with open("pages/example.md", "w") as f:
        f.write(s)
