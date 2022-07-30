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

    def read_contacts(
        self,
        field_name: str = None,
        field_value: Any = None
    ) -> DBResponse:
        try:
            data = json.loads(self._db_path.read_text())
            read_contacts = data["Contacts"]
        except json.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

        if field_name is None or field_value is None:
            return DBResponse(read_contacts, SUCCESS)

        filtered_contacts = [c for c in read_contacts if
                             field_name in c and
                             c[field_name] == field_value]
        return DBResponse(filtered_contacts, SUCCESS)

    def write_contacts(self, contact_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            data = json.loads(self._db_path.read_text())
            data["Contacts"] = contact_list
            new_data_str = json.dumps(data, indent=4)
            self._db_path.write_text(new_data_str)
            return DBResponse(new_data_str, SUCCESS)
        except OSError:
            return DBResponse(contact_list, DB_WRITE_ERROR)

    def delete_contacts(
        self,
        field_name: str = None,
        field_value: Any = None
    ) -> DBResponse:
        """
        Deletes all contacts with field_name and field_vale
        Returns deteleted contacts
        """
        try:
            data = json.loads(self._db_path.read_text())
            read_contacts = data["Contacts"]
        except json.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

        if field_name is None or field_value is None:
            kept_contacts, error = self.write_contacts([])
            return DBResponse(read_contacts, error)

        # TODO: there has to be a better solution than these loops
        keep_contacts = [c for c in read_contacts if
                         (field_name not in c) or
                         (field_name in c and
                          not c[field_name] == field_value)]
        delete_contacts = [c for c in read_contacts if
                           field_name in c and
                           c[field_name] == field_value]
        kept_contacts, error = self.write_contacts(keep_contacts)
        return DBResponse(delete_contacts, SUCCESS)

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
