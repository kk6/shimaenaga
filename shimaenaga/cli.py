import pathlib
import typer
from .core import main
from .generators import generate_markdown_template
from .initializers import initialize
from .config import default_config as dc
from .config import Config, SiteMeta

app = typer.Typer()


@app.command()
def init(
    site_title: str = typer.Option(dc.sitemeta.title, prompt="What's your site title?"),
    author: str = typer.Option(dc.sitemeta.author, prompt="What's your name?"),
    language_code: str = typer.Option(dc.sitemeta.language_code, prompt="Language code?"),
):
    """Initialize new site"""
    config = Config(theme=dc.theme, sitemeta=SiteMeta(title=site_title, author=author, language_code=language_code))
    initialize(config)
    typer.echo("New site initial setup complete✨")


@app.command()
def new(filename: str, title: str = "New title") -> None:
    """Create new page from template"""
    dirname = pathlib.Path("./posts")
    path = generate_markdown_template(dirname, title, filename)
    typer.echo(f"New markdown file created at {path}")


@app.command()
def build() -> None:
    """Build site"""
    typer.echo(f"Building...")
    main()
    typer.echo(f"Build finished!")
