import os
import pathlib
from typing import Dict, List, Optional, Tuple, Union

import tomlkit
from jinja2 import Environment, FileSystemLoader, Template

import mistune

ROOT_DIR = "."
TEMPLATE_DIR = "templates"
DEST_DIR = "dest"
PAGE_DIR = "pages"
POST_DIR = "posts"


def read_file(path: Union[pathlib.Path, str]) -> str:
    with open(path) as f:
        return f.read()


def parse_config(config_file: str) -> Dict:
    toml = read_file(config_file)
    return tomlkit.parse(toml)


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
    config: Dict,
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
            "site_metadata": config["metadata"],
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


def main() -> None:
    config = parse_config("config.toml")

    dirs = config["directory"]
    root_dir = pathlib.Path(dirs.get("root", ROOT_DIR))
    template_dir = root_dir / pathlib.Path(dirs.get("templates", TEMPLATE_DIR))
    dest_dir = root_dir / pathlib.Path(dirs.get("dest", DEST_DIR))
    pages_dir = root_dir / pathlib.Path(dirs.get("pages", PAGE_DIR))
    posts_dir = root_dir / pathlib.Path(dirs.get("posts", POST_DIR))

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


if __name__ == "__main__":
    main()
