import os
import pathlib
from typing import Dict

from jinja2 import Environment, FileSystemLoader, Template
import tomlkit

ROOT_DIR = "."
TEMPLATE_DIR = "templates"
DEST_DIR = "dest"


def parse_config(config_file: str) -> Dict:
    with open(config_file) as f:
        config = tomlkit.parse(f.read())
    return config


def get_template(template_path: pathlib.Path, filename: str) -> Template:
    env = Environment(loader=FileSystemLoader(str(template_path), encoding="utf8"))
    template = env.get_template(filename)
    return template


def dump_html(dest_dir: pathlib.Path, content: str, filename: str) -> None:
    if not dest_dir.exists():
        os.mkdir(dest_dir)
    with open(dest_dir / filename, mode="w") as f:
        f.write(str(content))


def main() -> None:
    config = parse_config("config.toml")

    dirs = config["directory"]
    root_dir = pathlib.Path(dirs.get("root", ROOT_DIR))
    template_dir = root_dir / pathlib.Path(dirs.get("templates", TEMPLATE_DIR))
    dest_dir = root_dir / pathlib.Path(dirs.get("dest", DEST_DIR))

    template = get_template(template_dir.resolve(), "index.j2")

    context = {"metadata": config["metadata"], "names": ["john", "alice"]}
    html = template.render(**context)
    dump_html(dest_dir, html, "index.html")


if __name__ == "__main__":
    main()
