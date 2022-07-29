"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc import config
from pcrmc.database import DBResponse, DatabaseHandler


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


class CurrentContact(NamedTuple):
    contact: Dict[str, Any]
    error: int


class Contacter:
    # TODO: rename to something better, maybe "Manager"
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def addMeeting(self, meeting: Dict[str, Any]) -> int:
        """Add new meeting"""
        relevant_contacts = meeting["Participants"]
        read = self._db_handler.read_contacts()
        if read.error != 0:
            return read.error

        for c in read.contact_list:
            if c["ID"] in relevant_contacts:
                c["Meetings"].append(meeting)

        write = self._db_handler.write_contacts(read.contact_list)
        return write.error

    def add(self,
            name: List[str],
            country: str,
            industry: str,
            meetings: List[Dict[str, Any]]
            ) -> CurrentContact:
        """Add a new contact to the database."""
        # TODO: Either replace str with List[str] or keep str everywhere
        name_text = " ".join(name)
        contact = {
                "ID": -1,
                "Name": name_text,
                "Country": country,
                "Industry": industry,
                "Meetings": meetings}
        read = self._db_handler.read_contacts()
        if read.error != 0:
            return CurrentContact(contact, read.error)

        contact["ID"] = \
            self._db_handler.get_new_contact_id(config.CONFIG_FILE_PATH)
        read.contact_list.append(contact)
        write = self._db_handler.write_contacts(read.contact_list)
        return CurrentContact(contact, write.error)

    def modify(self, id: int, field: str, value: str) -> DBResponse:
        read = self._db_handler.read_contacts()
        if read.error != 0:
            return read.error

        for c in read.contact_list:
            if c["ID"] == id:
                c[field] = value
        write = self._db_handler.write_contacts(read.contact_list)
        return write

    def get_contacts(self) -> DBResponse:
        """Return the current to-do list."""
        read = self._db_handler.read_contacts()
        return read
