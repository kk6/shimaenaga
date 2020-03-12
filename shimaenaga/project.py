import os
import pathlib
from typing import List
import shutil

from .renderers import Jinja2Renderer
from .files import write_file
from .page import load_pages
from .article import load_articles
from .config import Config


class Project:
    def __init__(self, config: Config):
        self.config = config
        self.renderer = Jinja2Renderer(config.theme)
        self.root_dir = pathlib.Path(".")
        self.pages_dir = self.root_dir / "pages"
        self.articles_dir = self.root_dir / "articles"
        self.dest_dir = self.root_dir / "dest"

        self.pages = load_pages(self.pages_dir)
        self.articles = load_articles(self.articles_dir)

    def build(self) -> None:
        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)
        self.build_index_page()
        self.build_pages()
        self.build_articles()
        self.copy_assets()

    def build_index_page(self) -> None:
        current_articles = {}
        for article in self.articles:
            link = article.path.with_suffix(".html")
            current_articles[link] = article.title

        context = {
            "sitemeta": self.config.sitemeta,
            "menus": self.get_menus(),
            "current_articles": current_articles,
        }
        html = self.renderer.render("index", context)
        write_file(self.dest_dir / "index.html", html)

    def build_pages(self) -> None:
        for page in self.pages:
            context = {
                "sitemeta": self.config.sitemeta,
                "menus": self.get_menus(),
                "page_title": page.title,
            }
            html = self.renderer.render("page", context)
            write_file(self.dest_dir / f"{page.name}.html", html)

    def build_articles(self) -> None:
        for article in self.articles:
            context = {
                "sitemeta": self.config.sitemeta,
                "menus": self.get_menus(),
                "article_title": article.title,
                "tags": article.tags,
            }
            html = self.renderer.render("article", context)
            dest_article_dir = self.dest_dir / article.path.parent
            if not dest_article_dir.exists():
                os.makedirs(dest_article_dir)
            write_file(dest_article_dir / f"{article.name}.html", html)

    def get_menus(self) -> List[str]:
        return [page.name for page in self.pages]

    def copy_assets(self) -> None:
        source_assets_dir = (
            self.renderer.themes_dir / self.config.theme / "assets"
        )  # FIXME: もうちょっとマシなロジック
        dest_assets_dir = self.dest_dir / "assets"
        if dest_assets_dir.exists():
            shutil.rmtree(dest_assets_dir)
        shutil.copytree(source_assets_dir, dest_assets_dir)
