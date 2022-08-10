"""This module provides the edit command"""
# pcrmc/view/edit.py

import typer
from pcrmc.view.utils import get_contacter, print_error
from pcrmc.view.console import console

app = typer.Typer()


@app.command("contact")
def edit_contact(
    id: int = typer.Option(..., "--id"),
    field: str = typer.Option(..., "--field", "-f"),
    value: str = typer.Option(..., "--value", "-v"),
) -> None:
    """Edit contact by id."""
    contacter = get_contacter()
    edited_contacts, error = contacter.edit_contact(
        id, field, value)

    if error:
        print_error(error)

    # should only run once for now
    for contact in edited_contacts:
        console.print(
            f'Contact {contact["Name"]} '
            f'with id {contact["ID"]} got edited:\n'
            f'"{field}" now has '
            f'value "{contact[field]}"'
        )


@app.command("meeting")
def edit_meeting(
    id: int = typer.Option(None, "--id"),
    field: str = typer.Option(..., "--field", "-f"),
    value: str = typer.Option(..., "--value", "-v")
) -> None:
    """Edit meeting by id."""
    contacter = get_contacter()
    edited_meetings, error = contacter.edit_meeting(
        id, field, value)

    if error:
        print_error(error)

    # should only run once for now
    for meeting in edited_meetings:
        console.print(
            f'Meeting with {meeting["ContactName"]} '
            f'and title {meeting["Title"]} '
            f'with id {meeting["ID"]} got edited:\n'
            f'"{field}" now has '
            f'value "{meeting[field]}"'
        )


if __name__ == "__main__":
    app()
