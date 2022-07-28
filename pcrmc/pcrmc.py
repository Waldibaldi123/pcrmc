"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc import DB_READ_ERROR
from pcrmc.database import DatabaseHandler

def generateMeeting(participants: List[int], date: str, loc: str, topics:List[str]) -> Dict[str, Any]:
        meeting = {"Participants": participants, "Date": date, "Loc":loc, "Topics":topics}
        return meeting

class CurrentContact(NamedTuple):
    contact: Dict[str, Any]
    error: int

class Contacter:
    # TODO: rename to something better, maybe "Manager"
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def addMeeting(self, meeting: Dict[str, Any]):
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
        

    def add(self, name: List[str], country: str, industry: str, meetings: List[Dict[str, Any]]) -> CurrentContact:
        """Add a new contact to the database."""
        # TODO: Change name type of List to str everywhere
        name_text = " ".join(name)
        contact = {
                "ID": -1,
                "Name": name_text,
                "Country": country,
                "Industry": industry,
                "Meetings": meetings
        }
        read = self._db_handler.read_contacts()
        # TODO: why specify DB_READ_ERROR, instead do != 0
        if read.error == DB_READ_ERROR:
            return CurrentContact(contact, read.error)
        contact["ID"] = len(read.contact_list)
        read.contact_list.append(contact)
        write = self._db_handler.write_contacts(read.contact_list)
        return CurrentContact(contact, write.error)

    def get_contacts(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_contacts()
        return read.contact_list