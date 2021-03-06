import os
import pathlib
import shutil
from typing import List

from loguru import logger

from .config import Config
from .contents import load_contents, Content, Article, sort_articles
from .files import write_file
from .renderers import Jinja2Renderer
from .paginator import Paginator


class Project:
    def __init__(self, config: Config):
        self.config = config
        self.renderer = Jinja2Renderer(config.theme)
        self.root_dir = pathlib.Path(".")
        self.pages_dir = self.root_dir / "pages"
        self.articles_dir = self.root_dir / "articles"
        self.dest_dir = self.root_dir / "dest"

        self.pages = load_contents(self.pages_dir, Content)
        self.articles = sort_articles(load_contents(self.articles_dir, Article))

    def build(self) -> None:
        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)
            logger.info("Created: {self.dest_dir}")
        self.build_index_page()
        logger.info("Index page built successfully.")
        self.build_pages()
        logger.info("Pages built successfully.")
        self.build_articles()
        logger.info("Articles built successfully.")
        self.copy_assets()
        logger.info("Copy of assets succeeded.")

    def build_index_page(self) -> None:
        paginator = Paginator(self.articles, self.config.sitemeta.per_page)
        for page in paginator.paginate():
            context = {
                "sitemeta": self.config.sitemeta,
                "menus": self.get_menus(),
                "articles": self.articles,
                "paginator": paginator,
                "page": page,
            }
            html = self.renderer.render("index", context)
            if page.current_page == 1:
                write_file(self.dest_dir / "index.html", html)
            else:
                if not os.path.exists(self.dest_dir / "page"):
                    os.mkdir(self.dest_dir / "page")
                write_file(self.dest_dir / "page" / f"{page.current_page}.html", html)

    def build_pages(self) -> None:
        for page in self.pages:
            context = {
                "sitemeta": self.config.sitemeta,
                "menus": self.get_menus(),
                "page": page,
            }
            html = self.renderer.render("page", context)
            write_file(self.dest_dir / f"{page.name}.html", html)

    def build_articles(self) -> None:
        for article in self.articles:
            context = {
                "sitemeta": self.config.sitemeta,
                "menus": self.get_menus(),
                "article": article,
            }
            html = self.renderer.render("article", context)
            dest_article_dir = self.dest_dir / article.path.parent
            if not dest_article_dir.exists():
                os.makedirs(dest_article_dir)
            output_article_path = dest_article_dir / f"{article.name}.html"
            write_file(output_article_path, html)
            logger.info(f"Article generated: {output_article_path}")
            self.copy_article_images(article, dest_article_dir)
            logger.info("Copied images used in the article")

    def get_menus(self) -> List[str]:
        return [page.name for page in self.pages]

    def copy_assets(self) -> None:
        source_assets_dir = self.renderer.themes_dir / self.config.theme / "assets"
        dest_assets_dir = self.dest_dir / "assets"
        if dest_assets_dir.exists():
            shutil.rmtree(dest_assets_dir)
        shutil.copytree(source_assets_dir, dest_assets_dir)

    def copy_article_images(self, article: Article, dest: pathlib.Path) -> None:
        images: List = []
        glob_patterns = ["*.jpg", "*.jpeg", "*.png", "*.svg"]
        for pattern in glob_patterns:
            images.extend(article.path.parent.glob(pattern))
        for image in images:
            shutil.copy(image, dest)
            logger.info(f"Copied image: {image}")
