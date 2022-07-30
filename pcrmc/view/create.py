"""This module provides the create command"""
# pcrmc/cli/create.py

from typing import List
import typer

app = typer.Typer()


@app.command()
def contact(identifier: List[str]):
    print(f"Creating contact: {identifier}")


@app.command()
def meeting(identifier: List[str]):
    print(f"Creating meeting: {identifier}")


if __name__ == "__main__":
    app()
