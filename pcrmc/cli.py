"""This module provides the pcrmc CLI"""
# pcrmc/cli.py

from pathlib import Path
from typing import List, Optional
import typer
from pcrmc import ERRORS, __app_name__, __version__, config, database, pcrmc
from datetime import datetime, date
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
def add_contact(name: List[str] = typer.Argument(...),
                country: str = typer.Option(str(), "--country", "-c"),
                industry: str = typer.Option(str(), "--industry", "-i")
                ) -> None:
    """Add a new contact with a NAME."""
    contacter = get_contacter()
    contact, error = contacter.add(name, country, industry)

    if error:
        typer.secho(
            f'Adding Contact failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"pcrmc: {contact['Name']} ({contact['Country']}"
            f" / {contact['Industry']}) was added",
            fg=typer.colors.GREEN,
        )


@app.command()
def modify_contact(id: int = typer.Argument(...),
                   field: str = typer.Option(str(), "--field", "-f"),
                   value: str = typer.Option(str(), "--value", "-v")
                   ) -> None:
    """Modify contact by id."""
    contacter = get_contacter()
    _, error = contacter.modify_contact(id, field, value)

    if error:
        typer.secho(
            f'modify_contact failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"pcrmc: Contact {id} modified",
            fg=typer.colors.GREEN,
        )


@app.command()
def rm_contact(id: int = typer.Argument(...)) -> None:
    """Delete contact by id."""
    contacter = get_contacter()
    _, error = contacter.delete_contact(id)

    if error:
        typer.secho(
            f'Dm_contact failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"pcrmc: Contact {id} removed",
            fg=typer.colors.GREEN,
        )


@app.command()
def add_meeting(
        participants: List[int] = typer.Argument(...),
        date: str = typer.Option(str(), "--date", "-d"),
        loc: str = typer.Option(str(), "--location", "-l"),
        topics: List[str] = typer.Option(str([]), "--topics", "-t")) -> None:
    """Add a new to-do with a DESCRIPTION."""
    contacter = get_contacter()
    meeting = pcrmc.generateMeeting(participants, date, loc, topics)

    contacts = contacter.get_contacts()
    if contacts.error:
        typer.secho(
            f'Adding Meeting failed with "{ERRORS[contacts.error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    part_names = [
        c["Name"] for c in contacts.data
        if c["ID"] in participants]

    error = contacter.addMeeting(meeting)

    if error:
        typer.secho(
            f'Adding Meeting failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f'pcrmc: Meeting between {" and ".join(part_names)} '
            f'at {loc} ({date}) was added',
            fg=typer.colors.GREEN,
        )


@app.command(name="list")
def list_all() -> None:
    """List all contacts."""
    contacter = get_contacter()
    contact_list, error = contacter.get_contacts()
    if error:
        typer.secho(
            f'Listing contacts failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if len(contact_list) == 0:
        typer.secho(
            "There are no contacts in the db", fg=typer.colors.RED
        )
        raise typer.Exit()

    # TODO: Darstellung optimieren.... Breite, Meetings?
    typer.secho("\nContacts:\n", fg=typer.colors.BLUE, bold=True)
    max_name_length = max([len(c["Name"]) for c in contact_list])
    columns = (
        "ID.  ",
        f"| Name  {(max_name_length-4) * ' '}",
        "| Country  ",
        "| Industry  ",
        "| Meetings  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for contact in contact_list:
        id = contact["ID"]
        name = contact["Name"]
        country = contact["Country"]
        industry = contact["Industry"]
        meetings = contact["Meetings"]
        color = typer.colors.BLUE
        if len(meetings) > 0:
            last_meeting = (max([m["Date"] for m in meetings]))
            days_since_meeting = abs((date.today()-datetime.strptime(
                last_meeting, "%Y%m%d").date()).days)

            if days_since_meeting < 10:
                color = typer.colors.GREEN
            elif days_since_meeting < 20:
                color = typer.colors.YELLOW
            elif days_since_meeting < 30:
                color = typer.colors.RED

        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {name}{(len(columns[1]) - len(str(name))-2) * ' '}"
            f"| {country}{(len(columns[2]) - len(str(country))-2) * ' '}"
            f"| {industry}{(len(columns[2]) - len(str(industry))-1) * ' '}"
            f"| {meetings}",
            fg=color,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


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
