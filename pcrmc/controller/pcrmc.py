"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc import SUCCESS, config
from pcrmc.model.database import DatabaseHandler


# TODO: needs to be tested
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

    def addMeeting(self, meeting: Dict[str, Any]) -> int:
        """Add new meeting"""
        response = self._db_handler.read_meetings()
        if response.error != SUCCESS:
            return ContacterResponse(response.data, response.error)
        meeting["ID"] = \
            self._db_handler.get_new_meeting_id(config.CONFIG_FILE_PATH)

        response.data.append(meeting)

        write = self._db_handler.write_meetings(response.data)
        return write.error

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
                "Industry": industry}
        read = self._db_handler.read_contacts()
        if read.error != SUCCESS:
            return ContacterResponse(contact, read.error)

        contact["ID"] = \
            self._db_handler.get_new_contact_id(config.CONFIG_FILE_PATH)
        read.data.append(contact)
        write = self._db_handler.write_contacts(read.data)
        return ContacterResponse(contact, write.error)

    def get_contacts(
            self,
            identifier: str = None
    ) -> ContacterResponse:
        """
        Returns contacts that match identifier (ID or name)
        Returns all contacts if no identifier is given
        """
        if identifier is None:
            contacts, error = self._db_handler.read_contacts()
        elif identifier.isdigit():
            contacts, error = self._db_handler.read_contacts(
                field_name="ID",
                field_value=int(identifier)
            )
        else:
            contacts, error = self._db_handler.read_contacts(
                field_name="Name",
                field_value=str(identifier)
            )
        return ContacterResponse(contacts, error)

    def modify_contact(self, id: int, field: str,
                       value: str) -> ContacterResponse:
        read = self._db_handler.read_contacts()
        if read.error != 0:
            return ContacterResponse(read.data, read.error)

        for c in read.data:
            if c["ID"] == id:
                c[field] = value
        write = self._db_handler.write_contacts(read.data)
        return ContacterResponse(write.data, write.error)

    def delete_contact(self, id: int) -> ContacterResponse:
        deleted_contact, error = self._db_handler.delete_contacts(
            field_name="ID",
            field_value=id
        )
        return ContacterResponse(deleted_contact, error)

    def get_meetings(self) -> ContacterResponse:
        """Return the current meeting list."""
        meetings, error = self._db_handler.read_meetings()
        return ContacterResponse(meetings, error)
