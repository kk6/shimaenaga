import typer
from .core import main

app = typer.Typer()


@app.command()
def new() -> None:
    """Create new page from template"""
    raise NotImplementedError


@app.command()
def build() -> None:
    """Build site"""
    typer.echo(f"Building...")
    main()
    typer.echo(f"Build finished!")
