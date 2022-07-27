"""This module provides the PCRMC model-controller."""
# pcrmc/pcrmc.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc import DB_READ_ERROR
from pcrmc.database import DatabaseHandler

class CurrentContact(NamedTuple):
    contact: Dict[str, Any]
    error: int

class Contacter:
    # TODO: rename to something better, maybe "Manager"
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, name: List[str], country: str, industry: str) -> CurrentContact:
        """Add a new contact to the database."""
        # TODO: Either replace str with List[str] or keep str everywhere
        name_text = " ".join(name)
        contact = {
                "Name": name_text,
                "Country": country,
                "Industry": industry,
        }
        read = self._db_handler.read_contacts()
        # TODO: why specify DB_READ_ERROR, instead do != 0
        if read.error == DB_READ_ERROR:
            return CurrentContact(contact, read.error)
        read.contact_list.append(contact)
        write = self._db_handler.write_contacts(read.contact_list)
        return CurrentContact(contact, write.error)
