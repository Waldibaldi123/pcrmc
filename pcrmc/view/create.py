"""This module provides the create command"""
# pcrmc/view/create.py

from typing import List
import typer
from pcrmc.view.utils import (
    format_argument_list, format_name_list,
    get_contacter, launch_editor, print_error)
from pcrmc import NO_NAME_OR_ID_ERROR
from pcrmc.view.console import console

app = typer.Typer()


@app.command("contact")
def add_contact(
        name: List[str] = typer.Argument(..., callback=format_argument_list),
        country: str = typer.Option(
            str(), "--country", "-c",
            prompt="Country?"
        ),
        industry: str = typer.Option(
            str(), "--industry", "-i",
            prompt="Industry?"
        )
) -> None:
    """Add a new contact with a NAME."""
    contacter = get_contacter()
    contact, error = contacter.add_contact(name, country, industry)

    if error:
        print_error(error)
    else:
        console.print(
            f'Contact {contact["Name"]} ({contact["Country"]}'
            f' / {contact["Industry"]}) was added '
            f'(id = {contact["ID"]})'
        )


# TODO: allow for additional IDs as well in case of duplicate names
@app.command("meeting")
def add_meeting(
    name: List[str] = typer.Argument(None, callback=format_argument_list),
    title: str = typer.Option(
        str(), "--title", '-t',
        prompt="title?"
    ),
    date: str = typer.Option(
        "today", "--date", "-d",
        prompt="date?"
    ),
    loc: str = typer.Option(
        str(), "--location", "-l",
        prompt="location?"
    ),
    id: int = typer.Option(None, "--id"),
    additional_names: List[str] = typer.Option(
        str(), "--additional-names", "-a",
        prompt="Additional Names (seperated with ,)?",
        callback=format_name_list
    )
) -> None:
    """Add a new meeting with a contact (name or id)."""
    if not name and id is None:
        print_error(NO_NAME_OR_ID_ERROR)

    desc = launch_editor()

    contacter = get_contacter()
    additional_names.insert(0, name)
    for idx, additional_name in enumerate(additional_names):
        if idx != 0:
            id = None

        meeting, error = contacter.add_meeting(
            name=additional_name,
            title=title,
            date=date,
            loc=loc,
            id=id,
            desc=desc
        )

        if error:
            try:
                print_error(error)
            except Exception:
                if idx < len(additional_names) - 1:
                    continue
                else:
                    raise typer.Exit(1)

        console.print(
            f'Meeting "{meeting["Title"]}" with {meeting["ContactName"]} '
            f'at {meeting["Loc"]} ({meeting["Date"]}) was added '
            f'(id = {meeting["ID"]})'
        )


if __name__ == "__main__":
    app()
