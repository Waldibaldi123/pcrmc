"""This module provides the show command"""
# pcrmc/view/show.py

from typing import List
import typer
from pcrmc.view.utils import get_contacter
from pcrmc import SUCCESS, ERRORS
from datetime import datetime, date

app = typer.Typer()

# TODO: seperate ouput if only one contact or one meeting is found
#       which shows all the details about the contact or meeting


@app.command("contact")
def show_contact(
    name: List[str] = typer.Argument(None),
    country: str = typer.Option(str(), "--country", "-c"),
    industry: str = typer.Option(str(), "--industry", "-i"),
    id: int = typer.Option(None, "--id")
) -> None:
    if name:
        name = " ".join(name)

    contacter = get_contacter()
    contact_list, error = contacter.get_contacts(
        name, country, industry, id)
    if error:
        typer.secho(
            f'Listing contacts failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    # TODO: Darstellung
    typer.secho("\nContacts:\n", fg=typer.colors.BLUE, bold=True)
    max_name_length = max([len(c["Name"]) for c in contact_list])
    columns = (
        "ID.  ",
        f"| Name  {(max_name_length-4) * ' '}",
        "| Country  ",
        "| Industry  "
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for contact in contact_list:
        id = contact["ID"]
        name = contact["Name"]
        country = contact["Country"]
        industry = contact["Industry"]

        color = typer.colors.BLUE
        # TODO
        # meetings, error = contacter.get_meetings()
        meetings, error = ([], SUCCESS)
        if error != SUCCESS:
            typer.secho(
                "Error reading meetings", fg=typer.colors.RED
            )
            raise typer.Exit()

        meetings = [m for m in meetings if id in m["Participants"]]
        if len(meetings) > 0:
            last_meeting = (max([m["Date"] for m in meetings]))
            days_since_meeting = abs((date.today()-datetime.strptime(
                last_meeting, "%Y%m%d").date()).days)

            if days_since_meeting < 10:
                color = typer.colors.GREEN
            elif days_since_meeting < 20:
                color = typer.colors.YELLOW
            elif days_since_meeting < 30:
                color = typer.colors.RED

        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {name}{(len(columns[1]) - len(str(name))-2) * ' '}"
            f"| {country}{(len(columns[2]) - len(str(country))-2) * ' '}"
            f"| {industry}{(len(columns[3]) - len(str(industry))-1) * ' '}",
            fg=color,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


@app.command("meeting")
def show_meetings(
    name: List[str] = typer.Argument(None),
    title: List[str] = typer.Option(str(), "--title", '-t'),
    date: str = typer.Option(str(), "--date", "-d"),
    loc: str = typer.Option(str(), "--location", "-l",),
    id: int = typer.Option(None, "--id")
) -> None:
    """List meetings."""
    if name:
        name = "".join(name)
    if title:
        title = "".join(title)

    contacter = get_contacter()
    meetings, error = contacter.get_meetings(
        name, title, date, loc, id)
    if error:
        typer.secho(
            f'Listing contacts failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    # TODO: Darstellung
    typer.secho("Meetings:\n", fg=typer.colors.BLUE, bold=True)
    max_name_length = max([len(c["ContactName"]) for c in meetings])
    columns = (
        "ID.  ",
        f"| Part.  {(max_name_length-5) * ' '}",
        "| Loc  ",
        "| Date     "
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for meeting in meetings:
        id = meeting["ID"]
        part = meeting["ContactName"]
        loc = meeting["Loc"]
        date = meeting["Date"]
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {part}{(len(columns[1]) - len(str(part))-2) * ' '}"
            f"| {loc}{(len(columns[2]) - len(str(loc))-2) * ' '}"
            f"| {date}{(len(columns[3]) - len(str(date))-2) * ' '}",
            fg=typer.colors.BLUE
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


# TODO: integrate this
# meetings = [m for m in meetings if id in m["Participants"]]
# if len(meetings) > 0:
#     last_meeting = (max([m["Date"] for m in meetings]))
#     days_since_meeting = abs((date.today()-datetime.strptime(
#         last_meeting, "%Y%m%d").date()).days)

#     if days_since_meeting < 10:
#         color = typer.colors.GREEN
#     elif days_since_meeting < 20:
#         color = typer.colors.YELLOW
#     elif days_since_meeting < 30:
#         color = typer.colors.RED


if __name__ == "__main__":
    app()
