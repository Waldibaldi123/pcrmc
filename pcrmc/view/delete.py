"""This module provides the delete command"""
# pcrmc/view/delete.py

from typing import List
import typer
from pcrmc.view.utils import get_contacter
from pcrmc import ERRORS

app = typer.Typer()


@app.command()
def contact(id: int = typer.Option(..., "--id")):
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


@app.command()
def meeting(identifier: List[str]):
    print(f"Deleting meeting: {identifier}")


if __name__ == "__main__":
    app()
