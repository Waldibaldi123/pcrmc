"""This module provides the show command"""
# pcrmc/view/show.py

from typing import List
import typer

app = typer.Typer()


@app.command()
def contact(identifier: List[str]):
    print(f"Showing contact: {identifier}")


@app.command()
def meeting(identifier: List[str]):
    print(f"Showing meeting: {identifier}")


if __name__ == "__main__":
    app()
