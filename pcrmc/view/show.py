"""This module provides the show command"""
# pcrmc/view/show.py

from typing import Any, List
import typer
from pcrmc.view.utils import format_argument_list, get_contacter, print_error
from pcrmc.view.console import console
from rich.table import Table
from datetime import datetime

app = typer.Typer()


def _print_contact_details(contact: Any) -> None:
    table = Table(title=contact["Name"])
    table.add_column("ID")
    table.add_column("Country")
    table.add_column("Industry")
    table.add_row(str(contact["ID"]), contact["Country"], contact["Industry"])
    console.line()
    console.print(table)


def _print_meeting_details(meeting: Any) -> None:
    table = Table(title=meeting["Title"])
    table.add_column("ID")
    table.add_column("Contact")
    table.add_column("Location")
    table.add_column("Date")
    table.add_row(
        str(meeting["ID"]),
        f'{meeting["ContactName"]} ({meeting["ContactID"]})',
        meeting["Loc"],
        meeting["Date"]
    )
    console.line()
    console.print(table)


def _print_contacts(contacts: List, contacts_meetings: List) -> None:
    table = Table(title="Contacts")
    table.add_column("<30 days", style="green")
    table.add_column("<90 days", style="yellow")
    table.add_column(">90 days", style="red")
    table.add_column(">180 days", style="blue")
    if len(contacts) == 0:
        console.print(table)
        return

    contact_day_sub_lists = [[], [], [], []]
    for idx, contact in enumerate(contacts):
        if not contacts_meetings[idx]:
            contact_day_sub_lists[3].append(contact)
            continue

        last_meeting = (max([datetime.strptime(m["Date"], "%Y-%m-%d")
                        for m in contacts_meetings[idx]]))
        days_since_meeting = (datetime.today() - last_meeting).days
        if days_since_meeting < 30:
            contact_day_sub_lists[0].append(contact)
        elif days_since_meeting < 90:
            contact_day_sub_lists[1].append(contact)
        elif days_since_meeting < 180:
            contact_day_sub_lists[2].append(contact)
        else:
            contact_day_sub_lists[3].append(contact)

    max_len = max(len(sub_list) for sub_list in contact_day_sub_lists)
    for sub_list in contact_day_sub_lists:
        sub_list += [{"Name": None, "ID": None}] * (max_len - len(sub_list))

    for sub_idx, _ in enumerate(contact_day_sub_lists[0]):
        row = []
        for idx, _ in enumerate(contact_day_sub_lists):
            if contact_day_sub_lists[idx][sub_idx]["ID"] is None:
                row.append(None)
            else:
                row.append(
                    f'({contact_day_sub_lists[idx][sub_idx]["ID"]}) '
                    f'{contact_day_sub_lists[idx][sub_idx]["Name"]}'
                )
        table.add_row(*row)

    console.line()
    console.print(table)


def _print_meetings(meetings: List) -> None:
    table = Table(title="Meetings")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("ContactName")
    table.add_column("Loc")
    table.add_column("Date")

    for meeting in meetings:
        table.add_row(
            str(meeting["ID"]),
            meeting["Title"],
            meeting["ContactName"],
            meeting["Loc"],
            meeting["Date"]
        )

    console.line()
    console.print(table)


@app.command("contact")
def show_contact(
    name: List[str] = typer.Argument(None, callback=format_argument_list),
    country: str = typer.Option(str(), "--country", "-c"),
    industry: str = typer.Option(str(), "--industry", "-i"),
    id: int = typer.Option(None, "--id")
) -> None:
    contacter = get_contacter()
    contacts, error = contacter.get_contacts(
        name, country, industry, id)
    if error:
        print_error(error)

    if len(contacts) == 1:
        _print_contact_details(contacts[0])
    else:
        contacts_meetings = []
        for contact in contacts:
            meetings, error = contacter.get_meetings(contact_id=contact["ID"])
            if error:
                print_error(error)
            contacts_meetings.append(meetings)
        _print_contacts(contacts, contacts_meetings)


@app.command("meeting")
def show_meetings(
    name: List[str] = typer.Argument(None, callback=format_argument_list),
    title: str = typer.Option(str(), "--title", '-t'),
    date: str = typer.Option(str(), "--date", "-d"),
    loc: str = typer.Option(str(), "--location", "-l",),
    id: int = typer.Option(None, "--id")
) -> None:
    """List meetings."""
    contacter = get_contacter()
    meetings, error = contacter.get_meetings(
        name=name,
        contact_id=None,    # TODO: give user option to ask give contact_id
        title=title,
        date=date,
        loc=loc,
        id=id
    )
    if error:
        print_error(error)

    if len(meetings) == 1:
        _print_meeting_details(meetings[0])
    else:
        _print_meetings(meetings)


if __name__ == "__main__":
    app()
