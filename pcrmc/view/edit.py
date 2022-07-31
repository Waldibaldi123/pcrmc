"""This module provides the edit command"""
# pcrmc/view/edit.py

from typing import List
import typer
from pcrmc.view.utils import get_contacter
from pcrmc import ERRORS

app = typer.Typer()


@app.command()
def contact(
    id: int,
    field: str = typer.Option(..., "--field", "-f"),
    value: str = typer.Option(..., "--value", "-v")
) -> None:
    """Edit contact by id."""
    contacter = get_contacter()
    edited_contacts, error = contacter.edit_contact(
        id, field, value)

    if error:
        typer.secho(
            f'edit_contact failed with "{ERRORS[error]}\n"',
            # f'Debug: response \n"{json.dumps(response, indent=4)}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    elif len(edited_contacts) == 0:
        typer.secho(
                f'pcrmc: contact with id {id} not found '
                f'or field  invalid\n'
                f'(adding new fields currently disabled '
                f'because it breaks show contact)',
                fg=typer.colors.GREEN,
            )
    else:
        # should only run once because ID is unique
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
