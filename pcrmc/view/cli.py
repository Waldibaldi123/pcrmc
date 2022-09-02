"""This module provides the pcrmc CLI"""
# pcrmc/cli/cli.py

from pathlib import Path
from typing import Optional
import typer
from pcrmc import config
from pcrmc import __app_name__, __version__
from pcrmc.model import database
from pcrmc.view import create, edit, show, delete
from pcrmc.view.utils import print_error
from pcrmc.view.console import console

app = typer.Typer()
app.add_typer(create.app, name="create")
app.add_typer(edit.app, name="edit")
app.add_typer(show.app, name="show")
app.add_typer(delete.app, name="delete")


@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_DIR_PATH),
            "--db-path",
            "-db",
            prompt="pcrmc database location?",
        ),
) -> None:
    """Initialize the pcrmc database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        print_error(app_init_error)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        print_error(db_init_error)
    else:
        console.print(f"The pcrmc database is {db_path}")


def _version_callback(value: bool) -> None:
    if value:
        console.print(f'{__app_name__} v{__version__}')
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
