"""This module provides the PCRMC database functionality"""
# pcrmc/database.py

import configparser
import json
from pathlib import Path
from typing import Any, NamedTuple
from pcrmc import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR,\
    SUCCESS, FILE_ERROR
from pcrmc import config

DEFAULT_DB_DIR_PATH = Path.home().joinpath(
        "." + Path.home().stem + "_pcrmc_db"
)
DB_FILE_NAMES = {
    "contact": "contacts.json",
    "meeting": "meetings.json"
}
DB_NEXT_ID_NAMES = {
    "contact": "NextCID",
    "meeting": "NextMID"
}


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the pcrmc database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the pcrmc database."""
    try:
        db_path.mkdir(exist_ok=True)
    except OSError:
        return FILE_ERROR
    for _, db_file_name in DB_FILE_NAMES.items():
        try:
            db_file_path = db_path / db_file_name
            db_file_path.touch(exist_ok=True)
        except OSError:
            return FILE_ERROR
        try:
            empty = []
            db_file_path.write_text(json.dumps(empty, indent=4))
        except OSError:
            return DB_WRITE_ERROR
    return SUCCESS


class DBResponse(NamedTuple):
    data: Any
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def _get_id_for_new_entry(
        self,
        table: str
    ) -> int:
        config_parser = configparser.ConfigParser()
        config_parser.read(config.CONFIG_FILE_PATH)

        next_id_name = DB_NEXT_ID_NAMES[table]
        id = int(config_parser["General"][next_id_name])
        config_parser["General"][next_id_name] = str(id + 1)
        try:
            with config.CONFIG_FILE_PATH.open("w") as file:
                config_parser.write(file)
        except OSError:
            return FILE_ERROR
        return id

    def _read(self, table: str) -> DBResponse:
        try:
            table_path = self._db_path / DB_FILE_NAMES[table]
            read_data = json.loads(table_path.read_text())
        except json.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)
        return DBResponse(read_data, SUCCESS)

    def _write(self, table: str, data: Any) -> DBResponse:
        try:
            table_path = self._db_path / DB_FILE_NAMES[table]
            table_path.write_text(json.dumps(data, indent=4))
        except json.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse(data, DB_WRITE_ERROR)
        return DBResponse(data, SUCCESS)

    def read(
        self,
        table: str,
        identifier_field: str = None,
        identifier_value: Any = None
    ) -> DBResponse:
        """
        Read table entries where identifier_field == identifier_value
        Read all table entries if no identifier given
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(read_data, error)

        if identifier_field is None or identifier_value is None:
            return DBResponse(read_data, SUCCESS)

        filtered_contacts = [c for c in read_data if
                             identifier_field in c and
                             c[identifier_field] == identifier_value]
        return DBResponse(filtered_contacts, SUCCESS)

    def insert(
        self,
        table: str,
        data: dict
    ) -> DBResponse:
        """
        Insert data into table
        Returns inserted data
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(data, error)

        data["ID"] = self._get_id_for_new_entry(table)
        read_data.append(data)
        _, error = self._write(table, read_data)
        return DBResponse(data, error)

    def update(
        self,
        table: str,
        identifier_field: str,
        identifier_value: Any,
        update_field: str,
        update_value: Any
    ) -> DBResponse:
        """
        Update table entries where identifier_field == identifier_value
        with update_field = update_value if update_field exists
        Returns updated entries
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(read_data, error)

        updated_entries = []
        for entry in read_data:
            if (identifier_field in entry and
                    entry[identifier_field] == identifier_value):
                if update_field in entry:
                    entry[update_field] = update_value
                    updated_entries.append(entry)

        _, error = self._write(table, read_data)
        return DBResponse(updated_entries, error)

    def delete(
        self,
        table: str,
        identifier_field: str = None,
        identifier_value: Any = None
    ) -> DBResponse:
        """
        Delete entries in table where identifier_name and identifier_value
        Delete all entries in table if no identifier is given
        Returns deteleted entries
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(read_data, error)

        if identifier_field is None or identifier_value is None:
            _, error = self._write(table, [])
            return DBResponse(read_data, error)

        # TODO: there has to be more pythonic solution than these loops
        keep_entries = [entry for entry in read_data if
                        (identifier_field not in entry) or
                        (identifier_field in entry and
                         not entry[identifier_field] == identifier_value)]
        delete_entries = [entry for entry in read_data if
                          identifier_field in entry and
                          entry[identifier_field] == identifier_value]
        _, error = self._write(table, keep_entries)
        return DBResponse(delete_entries, SUCCESS)
