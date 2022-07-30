"""This module provides the show command"""
# pcrmc/view/show.py

from typing import List
import typer
from pcrmc.view.utils import get_contacter
from pcrmc import ERRORS

app = typer.Typer()


@app.command("contact")
def show_contact(identifier_list: List[str] = typer.Argument(None)):
    identifier = None
    if identifier_list:
        identifier = " ".join(identifier_list)
    contacter = get_contacter()
    contact_list, error = contacter.get_contacts(identifier)
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
        name, country, industry, meetings = contact.values()
        typer.secho(
            # f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {name}{(len(columns[1]) - len(str(name))-2) * ' '}"
            f"| {country}{(len(columns[2]) - len(str(country))-2) * ' '}"
            f"| {industry}{(len(columns[2]) - len(str(industry))-1) * ' '}"
            f"| {meetings}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


@app.command()
def meeting(identifier: List[str]):
    print(f"Showing meeting: {identifier}")


if __name__ == "__main__":
    app()
