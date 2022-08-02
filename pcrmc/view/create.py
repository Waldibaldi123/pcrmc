"""This module provides the create command"""
# pcrmc/view/create.py

from typing import List
import typer
from pcrmc.view.utils import get_contacter
from pcrmc import ERRORS

app = typer.Typer()


@app.command("contact")
def add_contact(
        name_list: List[str] = typer.Argument(...),
        country: str = typer.Option(str(), "--country", "-c"),
        industry: str = typer.Option(str(), "--industry", "-i")
) -> None:
    """Add a new contact with a NAME."""
    name = " ".join(name_list)

    contacter = get_contacter()
    contact, error = contacter.add_contact(name, country, industry)

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


# TODO: allow multiple participants
@app.command("meeting")
def add_meeting(
    contact: List[str] = typer.Argument(...),
    title: List[str] = typer.Option(..., "--title", '-t', prompt="title?"),
    date: str = typer.Option(str(), "--date", "-d", prompt="date?"),
    loc: str = typer.Option(str(), "--location", "-l",  prompt="location?"),
    topics: List[str] = typer.Option([], "--topics", "-t",  prompt="topics?")
) -> None:
    """Add a new meeting with a CONTACT (name or id)."""
    contact = "".join(contact)
    title = "".join(title)

    contacter = get_contacter()
    meeting, error = contacter.add_meeting(
        contact_identifier=contact,
        title=title,
        date=date,
        loc=loc,
        topics=topics
    )

    if error:
        typer.secho(
            f'Adding Meeting failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    typer.secho(
        f'Meeting "{meeting["Title"]}" with {meeting["ContactName"]} '
        f'at {loc} ({date}) was added',
        fg=typer.colors.GREEN,
    )


if __name__ == "__main__":
    app()
