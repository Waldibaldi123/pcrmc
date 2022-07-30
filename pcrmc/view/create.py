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
    # TODO: figure out how List[str] acts if used more than once
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


@app.command("meeting")
def add_meeting(title: List[str]):
    print(f"Creating meeting: {title}")


if __name__ == "__main__":
    app()
