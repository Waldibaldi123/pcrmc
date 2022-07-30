# tests/test_pcrmc.py

import json
import pytest
from typer.testing import CliRunner
from pathlib import Path
from pcrmc import (
        SUCCESS,
        __app_name__,
        __version__,
        cli,
        pcrmc,
        config
)
runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f'{__app_name__} v{__version__}\n' in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    contact = {"Contacts": [
        {
            "Name": "Daniel Walder",
            "Country": "Austria",
            "Industry": "Software Engineering"
        }],
        "Meetings": []
        }
    db_file = tmp_path / "contact.json"
    with db_file.open("w") as db:
        json.dump(contact, db, indent=4)
    return db_file


test_data1 = {
        "ID": 24,
        "name": ["Daniel Walder"],
        "country": "Austria",
        "industry": "Software Engineering",
        "contact": {
            "Name": "Daniel Walder",
            "Country": "Austria",
            "Industry": "Software Engineering",

        }
}
test_data2 = {
        "ID": 25,
        "name": ["Roman Brock"],
        "country": "Austria",
        "industry": "Medicine",
        "contact": {
            "Name": "Roman Brock",
            "Country": "Austria",
            "Industry": "Medicine",

        }
}


@pytest.mark.parametrize(
        "name, country, industry, expected",
        [
            pytest.param(
                test_data1["name"],
                test_data1["country"],
                test_data1["industry"],
                (test_data1["contact"], SUCCESS),
            ),
            pytest.param(
                test_data2["name"],
                test_data2["country"],
                test_data2["industry"],
                (test_data2["contact"], SUCCESS),
            ),
        ],
)
@patch('pcrmc.config.CONFIG_FILE_PATH', mock_config_file)
def test_add(mock_json_file, name, country, industry, expected):
    contacter = pcrmc.Contacter(mock_json_file)
    ret, error = contacter.add(name, country, industry) 
    assert (ret, error) == expected
    read = contacter._db_handler.read_contacts()
    assert len(read.data) == 2
