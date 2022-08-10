"""This module provides the delete command"""
# pcrmc/view/delete.py

import typer
from pcrmc.view.utils import get_contacter, print_error
from pcrmc.view.console import console

app = typer.Typer()


@app.command("contact")
def delete_contact(id: int = typer.Option(..., "--id")):
    """Delete contact by id."""
    contacter = get_contacter()
    deleted_contacts, error = contacter.delete_contact(id)

    if error:
        print_error(error)

    # should only run once for now
    for contact in deleted_contacts:
        console.print(
            f'Contact {contact["Name"]} '
            f'with id {contact["ID"]} removed'
        )


@app.command("meeting")
def delete_meeting(id: int = typer.Option(..., "--id")):
    """Delete meeting by id."""
    contacter = get_contacter()
    deleted_meetings, error = contacter.delete_meeting(id)

    if error:
        print_error(error)

    # should only run once for now
    for meeting in deleted_meetings:
        console.print(
            f'Meeting with {meeting["ContactName"]} '
            f'with id {meeting["ID"]} removed'
        )


if __name__ == "__main__":
    app()
