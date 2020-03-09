import pathlib
import typer
from .core import main
from .generators import generate_template

app = typer.Typer()


@app.command()
def new(filename: str, title: str = "New title") -> None:
    """Create new page from template"""
    dirname = pathlib.Path("./posts")
    path = generate_template(dirname, title, filename)
    typer.echo(f"New markdown file created at {path}")


@app.command()
def build() -> None:
    """Build site"""
    typer.echo(f"Building...")
    main()
    typer.echo(f"Build finished!")
