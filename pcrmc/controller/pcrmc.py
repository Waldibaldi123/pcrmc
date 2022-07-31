"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc.model.database import DatabaseHandler


# TODO: needs to be moved
def generateMeeting(participants: List[int],
                    date: str,
                    loc: str,
                    topics: List[str]
                    ) -> Dict[str, Any]:
    meeting = {
        "ID": -1,
        "Participants": participants,
        "Date": date, "Loc": loc,
        "Topics": topics
        }
    return meeting


class ContacterResponse(NamedTuple):
    data: Any
    error: int


class Contacter:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add_contact(
            self,
            name: List[str],
            country: str,
            industry: str
    ) -> ContacterResponse:
        """Add a new contact to the database."""
        contact = {
            "Name": name,
            "Country": country,
            "Industry": industry
        }
        inserted_contact, error = self._db_handler.insert("contact", contact)
        return ContacterResponse(inserted_contact, error)

    def get_contacts(
            self,
            identifier: str = None
    ) -> ContacterResponse:
        """
        Returns contacts that match identifier (ID or name)
        Returns all contacts if no identifier is given
        """
        # TODO: be able to filter for multiple identifiers
        if identifier is None:
            contacts, error = self._db_handler.read("contact")
        elif identifier.isdigit():
            contacts, error = self._db_handler.read(
                "contact",
                identifier_name="ID",
                identifier_value=int(identifier)
            )
        else:
            contacts, error = self._db_handler.read(
                "contact",
                identifier_name="Name",
                identifier_value=str(identifier)
            )
        return ContacterResponse(contacts, error)

    def edit_contact(
        self,
        id: int,
        field: str,
        value: str
    ) -> ContacterResponse:

        edited_contacts, error = self._db_handler.update(
            "contact",
            identifier_field="ID",
            identifier_value=id,
            update_field=field,
            update_value=value
        )
        return ContacterResponse(edited_contacts, error)

    def delete_contact(self, id: int) -> ContacterResponse:
        deleted_contacts, error = self._db_handler.delete(
            "contact",
            identifier_field="ID",
            identifier_value=id
        )
        return ContacterResponse(deleted_contacts, error)
