"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, List, NamedTuple
from pcrmc import DUPLICATE_ERROR, NOT_FOUND_ERROR, SUCCESS
from pcrmc.model.database import DatabaseHandler


class ContacterResponse(NamedTuple):
    data: Any
    error: int


class Contacter:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def _get_contact_name_from_id(self, id: int) -> ContacterResponse:
        matched_contacts, error = self._db_handler.read(
            "contact",
            identifier_field="ID",
            identifier_value=id
        )
        if error:
            return ContacterResponse(str(), error)
        if len(matched_contacts) == 0:
            return ContacterResponse(matched_contacts, NOT_FOUND_ERROR)
        elif len(matched_contacts) > 1:
            return ContacterResponse(matched_contacts, DUPLICATE_ERROR)
        return ContacterResponse(matched_contacts[0]["Name"], SUCCESS)

    def _get_contact_id_from_name(self, name: str) -> ContacterResponse:
        matched_contacts, error = self._db_handler.read(
            "contact",
            identifier_field="Name",
            identifier_value=name
        )
        if error:
            return ContacterResponse(str(), error)
        if len(matched_contacts) == 0:
            return ContacterResponse(matched_contacts, NOT_FOUND_ERROR)
        elif len(matched_contacts) > 1:
            # TODO: allow for duplicate names
            return ContacterResponse(matched_contacts, DUPLICATE_ERROR)
        return ContacterResponse(matched_contacts[0]["ID"], SUCCESS)

    def add_contact(
        self,
        name: str,
        country: str,
        industry: str
    ) -> ContacterResponse:
        contact = {
            "Name": name,
            "Country": country,
            "Industry": industry
        }
        inserted_contact, error = self._db_handler.insert("contact", contact)
        return ContacterResponse(inserted_contact, error)

    def add_meeting(
        self,
        contact_identifier: str,
        title: str,
        date: str,
        loc: str,
        topics: List[str]
    ) -> ContacterResponse:
        if contact_identifier.isdigit():
            contact_id = contact_identifier
            contact_name, error = self._get_contact_name_from_id(contact_id)
        else:
            contact_name = contact_identifier
            contact_id, error = self._get_contact_id_from_name(contact_name)
        if error:
            return(str(), error)

        meeting = {
            "ContactName": contact_name,
            "ContactID": contact_id,
            "Title": title,
            "Date": date,
            "Loc": loc,
            "Topics": topics
        }
        inserted_meeting, error = self._db_handler.insert("meeting", meeting)
        return ContacterResponse(inserted_meeting, error)

    def get_contacts(
            self,
            name: str = None,
            country: str = None,
            industry: str = None,
            id: int = None
    ) -> ContacterResponse:
        contact_filter = {
            "Name": name,
            "Country": country,
            "Industry": industry,
            "ID": id
        }
        filter_fields = []
        filter_values = []
        for field in contact_filter:
            if contact_filter[field]:
                filter_fields.append(field)
                filter_values.append(contact_filter[field])

        contacts, error = self._db_handler.read(
            "contact",
            filter_fields=filter_fields,
            filter_values=filter_values
        )
        return ContacterResponse(contacts, error)

    def get_meetings(
            self,
            identifier: str = None
    ) -> ContacterResponse:
        # TODO: be able to filter for multiple identifiers
        if identifier is None:
            meetings, error = self._db_handler.read("meeting")
        elif identifier.isdigit():
            meetings, error = self._db_handler.read(
                "meeting",
                identifier_name="ID",
                identifier_value=int(identifier)
            )
        else:
            meetings, error = self._db_handler.read(
                "meeting",
                identifier_name="Title",
                identifier_value=str(identifier)
            )
        return ContacterResponse(meetings, error)

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

    def edit_meeting(
        self,
        id: int,
        field: str,
        value: str
    ) -> ContacterResponse:
        edited_meetings, error = self._db_handler.update(
            "meeting",
            identifier_field="ID",
            identifier_value=id,
            update_field=field,
            update_value=value
        )
        return ContacterResponse(edited_meetings, error)

    def delete_contact(self, id: int) -> ContacterResponse:
        deleted_contacts, error = self._db_handler.delete(
            "contact",
            identifier_field="ID",
            identifier_value=id
        )
        return ContacterResponse(deleted_contacts, error)

    def delete_meeting(self, id: int) -> ContacterResponse:
        deleted_meeting, error = self._db_handler.delete(
            "meeting",
            identifier_field="ID",
            identifier_value=id
        )
        return ContacterResponse(deleted_meeting, error)
