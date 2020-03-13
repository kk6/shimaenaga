import datetime
import pathlib
import typer
from .generators import generate_markdown_template, generate_article_template
from .initializer import initialize
from .config import default_config as dc
from .config import Config, SiteMeta

app = typer.Typer()


@app.command()
def init(
    site_title: str = typer.Option(dc.sitemeta.title, prompt="What's your site title?"),
    author: str = typer.Option(dc.sitemeta.author, prompt="What's your name?"),
    language_code: str = typer.Option(
        dc.sitemeta.language_code, prompt="Language code?"
    ),
) -> None:
    """Initialize new site"""
    config = Config(
        theme=dc.theme,
        sitemeta=SiteMeta(title=site_title, author=author, language_code=language_code),
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
    from .project import Project
    from .config import parse_config

    typer.echo(f"Load config file")
    config = parse_config("config.toml")
    typer.echo(f"Build start")
    project = Project(config)
    project.build()
    typer.echo(f"Build finished!")
