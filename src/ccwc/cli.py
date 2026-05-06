import typer

from .ccwc import ccwc 


app = typer.Typer()
app.command()(ccwc)


if __name__ == "__main__":
    app()
