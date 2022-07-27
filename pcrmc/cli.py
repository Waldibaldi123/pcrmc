"""This module provides the pcrmc CLI"""
# pcrmc/cli.py

from pathlib import Path
from typing import List, Optional
import typer
from pcrmc import ERRORS, __app_name__, __version__, config, database, pcrmc

app = typer.Typer()

@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="pcrmc database location?",
        ),
) -> None:
    """Initialize the pcrmc database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
                f'Creating config file failed with "{ERRORS[app_init_error]}"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
                f'Creating database failed with "{ERRORS[db_init_error]}"',
                typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The pcrmc database is {db_path}", fg=typer.colors.GREEN)

def get_contacter() -> pcrmc.Contacter:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
                'Config file not found. Please run "pcrmc init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return pcrmc.Contacter(db_path)
    else:
        typer.secho(
                'Database not found. Please run "pcrmc init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
        name: List[str] = typer.Argument(...),
        country: str = typer.Option("unknown", "--country", "-c"),
        industry: str = typer.Option("unknown", "--industry", "-i")
) -> None:
    """Add a new contact with a name."""
    contacter = get_contacter()
    contact, error = contacter.add(name, country, industry)
    if error:
        typer.secho(
                f'Adding contact failed with "{ERRORS[error]}"',
        )
        raise typer.Exit(1)
    else:
        typer.secho(
                f"""contact: "{contact['Name']}" was added """
                f"""with country "{contact['Country']}" and """
                f"""and industry "{contact['Industry']}".""",
                fg=typer.colors.GREEN,
        )

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
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

