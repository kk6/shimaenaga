import os
import pathlib
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader, Template
import tomlkit
import mistune

ROOT_DIR = "."
TEMPLATE_DIR = "templates"
DEST_DIR = "dest"
PAGE_DIR = "pages"
POST_DIR = "posts"


def parse_config(config_file: str) -> Dict:
    with open(config_file) as f:
        config = tomlkit.parse(f.read())
    return config


def get_template(template_path: pathlib.Path, filename: str) -> Template:
    env = Environment(loader=FileSystemLoader(str(template_path), encoding="utf8"))
    template = env.get_template(filename)
    return template


def get_pages(pages_path: pathlib.Path) -> List:
    page_names = os.listdir(pages_path)
    pages = []
    for page in page_names:
        path = pages_path / page
        if str(path).endswith(".md"):
            pages.append(path)
        else:
            if path.is_dir():
                posts = os.listdir(path)
                for post in posts:
                    pages.append(path / post)
    return pages


def get_posts(posts_path: pathlib.Path) -> List:
    _posts = os.listdir(posts_path)
    posts = []
    for post in _posts:
        posts.append(posts_path / post)
    return posts


def parse_markdown(markdown_path: pathlib.Path) -> str:
    with open(markdown_path) as f:
        html = mistune.html(f.read())
    return html


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
    pages_dir = root_dir / pathlib.Path(dirs.get("pages", PAGE_DIR))
    posts_dir = root_dir / pathlib.Path(dirs.get("posts", POST_DIR))

    template = get_template(template_dir.resolve(), "index.j2")

    markdowns = get_pages(pages_dir)
    posts = get_posts(posts_dir)
    markdowns.extend(posts)
    for md in markdowns:
        name, ext = md.name.split(".md")
        body = parse_markdown(md)
        context = {"metadata": config["metadata"], "body": body}
        html = template.render(**context)
        dump_html(dest_dir, html, f"{name}.html")


if __name__ == "__main__":
    main()
