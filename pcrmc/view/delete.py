"""This module provides the delete command"""
# pcrmc/view/delete.py

import typer
from pcrmc.view.utils import get_contacter
from pcrmc import ERRORS

app = typer.Typer()


@app.command("contact")
def delete_contact(id: int = typer.Option(..., "--id")):
    """Delete contact by id."""
    contacter = get_contacter()
    deleted_contacts, error = contacter.delete_contact(id)

    if error:
        typer.secho(
            f'delete_contact failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    # should only run once for now
    for contact in deleted_contacts:
        typer.secho(
            f'Contact {contact["Name"]} '
            f'with id {contact["ID"]} removed',
            fg=typer.colors.GREEN,
        )


@app.command("meeting")
def delete_meeting(id: int = typer.Option(..., "--id")):
    """Delete meeting by id."""
    contacter = get_contacter()
    deleted_meetings, error = contacter.delete_meeting(id)

    if error:
        typer.secho(
            f'delete_meeting failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    # should only run once for now
    for meeting in deleted_meetings:
        typer.secho(
            f'Meeting with {meeting["ContactName"]} '
            f'with id {meeting["ID"]} removed',
            fg=typer.colors.GREEN,
        )


if __name__ == "__main__":
    app()
