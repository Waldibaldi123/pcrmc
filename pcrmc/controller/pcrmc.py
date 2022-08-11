"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, NamedTuple
from pcrmc import BAD_INPUT_ERROR, DUPLICATE_ERROR, NOT_FOUND_ERROR, SUCCESS
from pcrmc.model.database import DatabaseHandler
from datetime import datetime, timedelta


class ContacterResponse(NamedTuple):
    data: Any
    error: int


class Contacter:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def _get_contact_name_from_id(self, id: int) -> ContacterResponse:
        matched_contacts, error = self.get_contacts(
            id=id
        )
        if error:
            return ContacterResponse(str(), error)
        if len(matched_contacts) == 0:
            return ContacterResponse(matched_contacts, NOT_FOUND_ERROR)
        elif len(matched_contacts) > 1:
            return ContacterResponse(matched_contacts, DUPLICATE_ERROR)
        return ContacterResponse(matched_contacts[0]["Name"], SUCCESS)

    def _get_contact_id_from_name(self, name: str) -> ContacterResponse:
        matched_contacts, error = self.get_contacts(
            name=name
        )
        if error:
            return ContacterResponse(str(), error)
        if len(matched_contacts) == 0:
            return ContacterResponse(matched_contacts, NOT_FOUND_ERROR)
        elif len(matched_contacts) > 1:
            # TODO: allow for duplicate names
            return ContacterResponse(matched_contacts, DUPLICATE_ERROR)
        return ContacterResponse(matched_contacts[0]["ID"], SUCCESS)

    def _format_date(self, date: str) -> ContacterResponse:
        if date == "today" or not date:
            formatted_date = datetime.today().strftime('%Y-%m-%d')
        elif date == "yesterday":
            yesterday = datetime.today() - timedelta(1)
            formatted_date = yesterday.strftime('%Y-%m-%d')
        else:
            try:
                datetime.strptime(date, '%Y-%m-%d')
                formatted_date = date
            except ValueError:
                return ContacterResponse(date, BAD_INPUT_ERROR)
        return ContacterResponse(formatted_date, SUCCESS)

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
        name: str,
        title: str,
        date: str,
        loc: str,
        id: int,
        desc: str
    ) -> ContacterResponse:
        if name:
            id, error = self._get_contact_id_from_name(name)
        elif id is not None:
            # override name with name from given id
            name, error = self._get_contact_name_from_id(id)
        if error:
            return ContacterResponse(str(), error)

        formatted_date, error = self._format_date(date)
        if error:
            return ContacterResponse(formatted_date, error)

        meeting = {
            "ContactName": name,
            "ContactID": id,
            "Title": title,
            "Date": formatted_date,
            "Loc": loc,
            "Description": desc
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
            if contact_filter[field] or contact_filter[field] == 0:
                filter_fields.append(field)
                filter_values.append(contact_filter[field])

        contacts, error = self._db_handler.filter(
            "contact",
            filter_fields=filter_fields,
            filter_values=filter_values
        )
        return ContacterResponse(contacts, error)

    def get_meetings(
        self,
        name: str = None,
        contact_id: int = None,
        title: str = None,
        date: str = None,
        loc: str = None,
        id: int = None
    ) -> ContacterResponse:
        # TODO: differentiate better between meeting id and contact id
        meeting_filter = {
            "ContactName": name,
            "ContactID": contact_id,
            "Title": title,
            "Date": date,
            "Loc": loc,
            "ID": id
        }
        filter_fields = []
        filter_values = []
        for field in meeting_filter:
            if meeting_filter[field] or meeting_filter[field] == 0:
                filter_fields.append(field)
                filter_values.append(meeting_filter[field])

        meetings, error = self._db_handler.filter(
            "meeting",
            filter_fields=filter_fields,
            filter_values=filter_values
        )
        return ContacterResponse(meetings, error)

    def edit_contact(
        self,
        id: int,
        edit_field: str,
        edit_value: Any
    ) -> ContacterResponse:
        edited_contacts, error = self._db_handler.update(
            "contact",
            id=id,
            update_field=edit_field,
            update_value=edit_value
        )
        return ContacterResponse(edited_contacts, error)

    def edit_meeting(
        self,
        id: int,
        edit_field: str,
        edit_value: Any
    ) -> ContacterResponse:
        if edit_field == "Date":
            edit_value, error = self._format_date(edit_value)
        if error:
            return ContacterResponse(edit_field, error)

        edited_meetings, error = self._db_handler.update(
            "meeting",
            id=id,
            update_field=edit_field,
            update_value=edit_value
        )
        return ContacterResponse(edited_meetings, error)

    def delete_contact(self, id: int) -> ContacterResponse:
        deleted_contacts, error = self._db_handler.delete(
            "contact",
            id=id
        )
        return ContacterResponse(deleted_contacts, error)

    def delete_meeting(self, id: int) -> ContacterResponse:
        deleted_meeting, error = self._db_handler.delete(
            "meeting",
            id=id
        )
        return ContacterResponse(deleted_meeting, error)
