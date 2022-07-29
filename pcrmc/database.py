"""This module provides the PCRMC database functionality"""
# pcrmc/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
        "." + Path.home().stem + "_pcrmc.json"
)


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the pcrmc database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the pcrmc database."""
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    data: Any
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_contacts(self) -> DBResponse:
        try:
            contacts_json = json.loads(self._db_path.read_text())
            return DBResponse(contacts_json, SUCCESS)
        except json.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_contacts(self, contact_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            contact_str = json.dumps(contact_list, indent=4)
            self._db_path.write_text(contact_str)
            return DBResponse(contact_str, SUCCESS)
        except OSError:
            return DBResponse(contact_list, DB_WRITE_ERROR)

    # see database_struct.json for database structure
    # TODO: read all contact names and IDs
    # TODO: read contact details given contact ID
    # TODO: write specific contact details
    # TODO: read all meeting titles, Dates and IDs
    # TODO: read meeting details given meeting ID
    # TODO: write meetings to append new meeting
    # TODO: read contact names and IDs given detail field/value pair
