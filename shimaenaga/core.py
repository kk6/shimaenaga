import os
import pathlib
import shutil
from typing import Dict, List, Optional, Tuple

import tomlkit
from jinja2 import Environment, FileSystemLoader, Template

import mistune

from .config import parse_config, Config
from .files import read_file


ROOT_DIR = pathlib.Path(".")
THEMES_DIR = pathlib.Path(__file__).parent / "themes"


def get_template(template_path: pathlib.Path, filename: str) -> Template:
    env = Environment(loader=FileSystemLoader(str(template_path), encoding="utf8"))
    template = env.get_template(filename)
    return template


def get_markdowns(parent: pathlib.Path) -> List:
    markdowns = []
    for child in os.listdir(parent):
        path = parent / child
        if str(path).endswith(".md"):
            markdowns.append(path)
    return markdowns


def parse_markdown(markdown_path: pathlib.Path) -> Tuple[Optional[Dict], str]:
    text = read_file(markdown_path)
    if text.startswith("+++\n"):
        _, meta_text, markdown = text.split("+++\n")
        metadata = tomlkit.parse(meta_text)
    else:
        metadata = None
        markdown = text
    html = mistune.html(markdown)
    return metadata, html


def dump_html(dest_dir: pathlib.Path, content: str, filename: str) -> None:
    if not dest_dir.exists():
        os.mkdir(dest_dir)
    with open(dest_dir / filename, mode="w") as f:
        f.write(str(content))


def generate(
    paths: List,
    config: Config,
    template: Template,
    dest_dir: pathlib.Path,
    menus: List,
    dirname: str = None,
    post_links: Dict = None,
) -> None:
    for path in paths:
        name, ext = path.name.split(".md")
        metadata, body = parse_markdown(path)
        if name != "index":
            post_links = {}
        context = {
            "sitemeta": config.sitemeta,
            "metadata": metadata,
            "body": body,
            "menus": menus,
            "post_links": post_links,
        }
        html = template.render(**context)
        outfile = f"{name}.html"
        if dirname:
            outfile = os.path.join(dirname, outfile)
        dump_html(dest_dir, html, outfile)


def copy_assets(source_assets_dir: pathlib.Path, dest_dir: pathlib.Path) -> None:
    dest_assets_dir = dest_dir / "assets"
    if dest_assets_dir.exists():
        shutil.rmtree(dest_assets_dir)
    shutil.copytree(source_assets_dir, dest_assets_dir)


def main() -> None:
    config = parse_config("config.toml")

    theme = config.theme

    template_dir = THEMES_DIR / theme / "templates"
    pages_dir = ROOT_DIR / "pages"
    posts_dir = ROOT_DIR / "posts"
    dest_dir = ROOT_DIR / "dest"

    page_template = get_template(template_dir.resolve(), "page.j2")
    post_template = get_template(template_dir.resolve(), "post.j2")

    pages = get_markdowns(pages_dir)
    menus = [p.name[:-3] for p in pages]

    posts = get_markdowns(posts_dir)
    post_links = {}
    for post in posts:
        metadata, _ = parse_markdown(post)
        post_links[post.name.replace(".md", ".html")] = metadata["title"]  # type: ignore
    output_post_dir = dest_dir / "posts"
    if not output_post_dir.exists():
        os.makedirs(output_post_dir)

    generate(pages, config, page_template, dest_dir, menus, post_links=post_links)
    generate(posts, config, post_template, dest_dir, menus, dirname="posts")

    source_assets_dir = THEMES_DIR / theme / "assets"
    copy_assets(source_assets_dir, dest_dir)
