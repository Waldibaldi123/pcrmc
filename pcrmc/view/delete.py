"""This module provides the delete command"""
# pcrmc/view/delete.py

from typing import List
import typer

app = typer.Typer()


@app.command()
def contact(identifier: List[str]):
    print(f"Deleting contact: {identifier}")


@app.command()
def meeting(identifier: List[str]):
    print(f"Deleting meeting: {identifier}")


if __name__ == "__main__":
    app()
