"""This module provides the edit command"""
# pcrmc/view/edit.py

from typing import List
import typer
from pcrmc.view.utils import get_contacter
from pcrmc import ERRORS

app = typer.Typer()


@app.command()
def contact(
    name: List[str] = typer.Argument(None),
    field: str = typer.Option(..., "--field", "-f"),
    value: str = typer.Option(..., "--value", "-v"),
    id: int = typer.Option(None, "--id")
) -> None:
    """Edit contact by id."""
    if name:
        name = " ".join(name)
    if not name and not id:
        typer.secho(
            'Must give either name or id',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    contacter = get_contacter()
    edited_contacts, error = contacter.edit_contact(
        name, field, value, id)

    if error:
        typer.secho(
            f'edit_contact failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    # should only run once for now
    for contact in edited_contacts:
        typer.secho(
            f'pcrmc: Contact {contact["Name"]} '
            f'with id {contact["ID"]} got edited:\n'
            f'"{field}" now has '
            f'value "{contact[field]}"',
            fg=typer.colors.GREEN,
        )


@app.command()
def meeting(identifier: List[str]):
    print(f"Editing meeting: {identifier}")


if __name__ == "__main__":
    app()
