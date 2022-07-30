"""Pcrmc entry point script."""
# pcrmc/__main__.py

from pcrmc import __app_name__
from pcrmc.view import cli


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
