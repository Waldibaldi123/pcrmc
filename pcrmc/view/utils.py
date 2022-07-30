"""This module provides helper methods for the view layer"""
# pcrmc/view/utils.py

import typer
from pcrmc import config
from pcrmc.controller import pcrmc
from pcrmc.model import database


def get_contacter() -> pcrmc.Contacter:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
                'Config file not found. Please run "pcrmc init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return pcrmc.Contacter(db_path)
    else:
        typer.secho(
                'Database not found. Please run "pcrmc init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
