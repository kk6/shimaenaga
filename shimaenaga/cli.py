import datetime
import pathlib

import typer
from livereload import Server
from loguru import logger

from .config import Config, SiteMeta
from .config import default_config as dc
from .config import parse_config
from .generators import generate_markdown_template, generate_article_template
from .initializer import initialize
from .project import Project

app = typer.Typer()


@app.command()
def init(
    site_title: str = typer.Option(dc.sitemeta.title, prompt="What's your site title?"),
    author: str = typer.Option(dc.sitemeta.author, prompt="What's your name?"),
    language_code: str = typer.Option(
        dc.sitemeta.language_code, prompt="Language code?"
    ),
    per_page: int = typer.Option(dc.sitemeta.per_page, prompt="How many articles per page?"),
) -> None:
    """Initialize new site"""
    config = Config(
        theme=dc.theme,
        sitemeta=SiteMeta(title=site_title, author=author, language_code=language_code, per_page=per_page),
    )
    initialize(config)
    typer.echo("New site initial setup complete ✨")


@app.command()
def new(filename: str, title: str = "New title", page: bool = False) -> None:
    """Create new page from template"""
    if page:
        dirname = pathlib.Path("./pages")
        path = generate_markdown_template(dirname, title, filename)
    else:
        local_time = datetime.date.today()
        dirname = pathlib.Path(".")
        path = generate_article_template(dirname, title, filename, local_time)
    typer.echo(f"New markdown file created at {path}")


@app.command()
def build() -> None:
    """Build project"""
    logger.info("Building project...")
    config = parse_config("config.toml")
    project = Project(config)
    project.build()
    logger.success("Build completed")


@app.command()
def serve() -> None:
    server = Server()
    logger.info("Starting live-reload...")
    server.watch("articles/", build)
    server.watch("pages/", build)
    server.watch("config.toml", build)
    server.serve(root="dest")
