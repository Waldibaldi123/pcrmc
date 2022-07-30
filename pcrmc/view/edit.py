"""This module provides the edit command"""
# pcrmc/view/edit.py

from typing import List
import typer

app = typer.Typer()


@app.command()
def contact(identifier: List[str]):
    print(f"Editing contact: {identifier}")


@app.command()
def meeting(identifier: List[str]):
    print(f"Editing meeting: {identifier}")


if __name__ == "__main__":
    app()
