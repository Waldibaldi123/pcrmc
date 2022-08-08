"""This module provides the PCRMC database functionality"""
# pcrmc/database.py

import configparser
import json
from pathlib import Path
from typing import Any, List, NamedTuple
from pcrmc import BAD_INPUT_ERROR, DB_READ_ERROR, DB_WRITE_ERROR, \
    DUPLICATE_ERROR, JSON_ERROR, NOT_FOUND_ERROR, SUCCESS, FILE_ERROR
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

    def read(
        self,
        table: str,
        id: int
    ) -> DBResponse:
        """
        Returns row in table where ID == id
        Returns error if multiple or no matches
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(read_data, error)

        filtered_data = [row for row in read_data if row["ID"] == id]
        if len(filtered_data) == 0:
            return DBResponse(filtered_data, NOT_FOUND_ERROR)
        elif len(filtered_data) > 1:
            return DBResponse(filtered_data, DUPLICATE_ERROR)
        return DBResponse(filtered_data, SUCCESS)

    def update(
        self,
        table: str,
        id: int,
        update_field: str,
        update_value: Any
    ) -> DBResponse:
        """
        Update row in table where ID == id
        with update_field = update_value if update_field exists
        Returns updated entry
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(read_data, error)

        updated_entries = []
        for row in read_data:
            if (row["ID"] == id):
                if update_field in row:
                    row[update_field] = update_value
                    updated_entries.append(row)

        if len(updated_entries) == 0:
            return DBResponse(updated_entries, NOT_FOUND_ERROR)
        elif len(updated_entries) > 1:
            return DBResponse(updated_entries, DUPLICATE_ERROR)

        _, error = self._write(table, read_data)
        return DBResponse(updated_entries, error)

    def delete(
        self,
        table: str,
        id: int
    ) -> DBResponse:
        """
        Delete row in table where ID == id
        Returns deteleted row
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(read_data, error)

        keep_rows = []
        delete_rows = []
        for row in read_data:
            if (row["ID"] == id):
                delete_rows.append(row)
            else:
                keep_rows.append(row)

        if len(delete_rows) == 0:
            return DBResponse(delete_rows, NOT_FOUND_ERROR)
        elif len(delete_rows) > 1:
            return DBResponse(delete_rows, DUPLICATE_ERROR)

        _, error = self._write(table, keep_rows)
        return DBResponse(delete_rows, SUCCESS)

    def filter(
        self,
        table: str,
        filter_fields: List[str] = [],
        filter_values: List[Any] = []
    ) -> DBResponse:
        """
        Read table entries where identifier_field == identifier_value
        Read all table entries if no identifier given
        """
        read_data, error = self._read(table)
        if error:
            return DBResponse(read_data, error)
        if len(filter_fields) != len(filter_values):
            return DBResponse(read_data, BAD_INPUT_ERROR)

        if not filter_fields or not filter_values:
            return DBResponse(read_data, SUCCESS)

        filtered_data = read_data
        for idx, _ in enumerate(filter_fields):
            filtered_data = [
                d for d in filtered_data if
                filter_fields[idx] in d and
                d[filter_fields[idx]] == filter_values[idx]
            ]
        if len(filtered_data) == 0:
            return DBResponse(filtered_data, NOT_FOUND_ERROR)
        return DBResponse(filtered_data, SUCCESS)
