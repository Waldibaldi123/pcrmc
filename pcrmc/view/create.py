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
            f"Contact {contact['Name']} ({contact['Country']}"
            f" / {contact['Industry']}) was added",
            fg=typer.colors.GREEN,
        )


# TODO: allow multiple participants
@app.command("meeting")
def add_meeting(
    name: List[str] = typer.Argument(None),
    title: List[str] = typer.Option(..., "--title", '-t', prompt="title?"),
    date: str = typer.Option(str(), "--date", "-d", prompt="date?"),
    loc: List[str] = typer.Option(str(), "--location", "-l", prompt="location?"),  # noqa: E501
    id: int = typer.Option(None, "--id")
) -> None:
    """Add a new meeting with a contact (name or id)."""
    if name:
        name = " ".join(name)
    title = "".join(title)
    loc = "".join(loc)
    if not name and id is None:
        typer.secho(
            'Must give either name or id',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    contacter = get_contacter()
    meeting, error = contacter.add_meeting(
        name=name,
        title=title,
        date=date,
        loc=loc,
        id=id
    )

    if error:
        typer.secho(
            f'Adding Meeting failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    typer.secho(
        f'Meeting "{meeting["Title"]}" with {meeting["ContactName"]} '
        f'at {meeting["Loc"]} ({meeting["Date"]}) was added',
        fg=typer.colors.GREEN,
    )


if __name__ == "__main__":
    app()
