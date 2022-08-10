"""This module provides helper methods for the view layer"""
# pcrmc/view/utils.py

import typer
from pcrmc import config
from pcrmc.controller import pcrmc
from pcrmc.model import database
from pcrmc import ERRORS, NO_INIT_ERROR
from pcrmc.view.console import error_console
from typing import List


def print_error(error: int) -> None:
    """Print error and exit"""
    error_console.print(ERRORS[error], style="red")
    raise typer.Exit(1)


def get_contacter() -> pcrmc.Contacter:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        print_error(NO_INIT_ERROR)
    if db_path.exists():
        return pcrmc.Contacter(db_path)
    else:
        print_error(NO_INIT_ERROR)


def format_name_list(names: List[str]) -> List[str]:
    joined_names = "".join(names)
    split_names = joined_names.split(",")
    stripped_names = [name.strip() for name in split_names]
    return stripped_names
