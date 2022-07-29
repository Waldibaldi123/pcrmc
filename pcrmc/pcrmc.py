"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc import SUCCESS
from pcrmc.database import DatabaseHandler


# TODO: needs to be tested
def generateMeeting(participants: List[int],
                    date: str,
                    loc: str,
                    topics: List[str]
                    ) -> Dict[str, Any]:
    meeting = {
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
        relevant_contacts = meeting["Participants"]
        read = self._db_handler.read_contacts()
        if read.error != SUCCESS:
            return read.error

        for c in read.data:
            if c["ID"] in relevant_contacts:
                c["Meetings"].append(meeting)

        write = self._db_handler.write_contacts(read.data)
        return write.error

    def add(self,
            name: List[str],
            country: str,
            industry: str
            ) -> ContacterResponse:
        """Add a new contact to the database."""
        # TODO: Either replace str with List[str] or keep str everywhere
        name_text = " ".join(name)
        contact = {
                "Name": name_text,
                "Country": country,
                "Industry": industry,
                "Meetings": []}
        read = self._db_handler.read_contacts()
        if read.error != SUCCESS:
            return ContacterResponse(contact, read.error)
        # TODO: this breaks/duplicates an ID if we remove and then add a contact # noqa: E501
        # contact["ID"] = len(read.contact_list)
        read.data.append(contact)
        write = self._db_handler.write_contacts(read.data)
        return ContacterResponse(contact, write.error)

    def get_contacts(self) -> ContacterResponse:
        """Return the current to-do list."""
        contacts, error = self._db_handler.read_contacts()
        return ContacterResponse(contacts, error)
