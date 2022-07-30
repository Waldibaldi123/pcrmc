"""This module provides the PCRMC database functionality"""
# pcrmc/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from pcrmc import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR,\
     SUCCESS, FILE_ERROR

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
        empty = {'Contacts': [], 'Meetings': []}
        db_path.write_text(json.dumps(empty, indent=4))
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
            data = json.loads(self._db_path.read_text())
            contacts_json = data["Contacts"]
            return DBResponse(contacts_json, SUCCESS)
        except json.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_contacts(self, contact_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            data = json.loads(self._db_path.read_text())
            data["Contacts"] = contact_list
            new_data_str = json.dumps(data, indent=4)
            self._db_path.write_text(new_data_str)
            return DBResponse(new_data_str, SUCCESS)
        except OSError:
            return DBResponse(contact_list, DB_WRITE_ERROR)

    def read_meetings(self) -> DBResponse:
        try:
            data = json.loads(self._db_path.read_text())
            meetings_json = data["Meetings"]
            return DBResponse(meetings_json, SUCCESS)
        except json.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_meetings(self, meeting_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            data = json.loads(self._db_path.read_text())
            data["Meetings"] = meeting_list
            new_data_str = json.dumps(data, indent=4)
            self._db_path.write_text(new_data_str)
            return DBResponse(new_data_str, SUCCESS)
        except OSError:
            return DBResponse(meeting_list, DB_WRITE_ERROR)

    def get_new_contact_id(self, config_file: Path) -> int:
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        id = int(config_parser["General"]["NextCID"])
        config_parser["General"]["NextCID"] = str(id + 1)
        try:
            with config_file.open("w") as file:
                config_parser.write(file)
        except OSError:
            return FILE_ERROR
        return id

    def get_new_meeting_id(self, config_file: Path) -> int:
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        id = int(config_parser["General"]["NextMID"])
        config_parser["General"]["NextMID"] = str(id + 1)
        try:
            with config_file.open("w") as file:
                config_parser.write(file)
        except OSError:
            return FILE_ERROR
        return id
    # see database_struct.json for database structure
    # TODO: read all contact names and IDs
    # TODO: read contact details given contact ID
    # TODO: write specific contact details
    # TODO: read all meeting titles, Dates and IDs
    # TODO: read meeting details given meeting ID
    # TODO: write meetings to append new meeting
    # TODO: read contact names and IDs given detail field/value pair
