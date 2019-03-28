import json
import pathlib

import pytest
import yaml

from districtr_process.columns import Column
from districtr_process.exceptions import MissingColumnsError
from districtr_process.place import Election, Place, PlaceSchema, Population
from districtr_process.column_set import summarize_column, ColumnSetSchema


@pytest.fixture
def lowell():
    with open("data/lowell.yml") as f:
        lowell_yaml = yaml.safe_load(f)
    return PlaceSchema().load(lowell_yaml)


@pytest.fixture
def ma_precincts():
    with open("data/ma_precincts_02_10.yml") as f:
        ma_yaml = yaml.safe_load(f)
    return PlaceSchema().load(ma_yaml)


@pytest.fixture
def data_files():
    def generator():
        for filename in pathlib.Path("data").iterdir():
            if filename.suffix in ("yml", "yaml"):
                with open(filename) as f:
                    yield yaml.safe_load(f)
            elif filename.suffix == "json":
                with open(filename) as f:
                    yield json.load(f)

    return generator


def test_lists_of_columns_deserialize():
    schema = ColumnSetSchema()
    raw = {
        "metadata": {"year": 2000, "race": "Presidential"},
        "subgroups": [
            {"name": "Republican", "key": "R_VOTES"},
            {"name": "Democratic", "key": "D_VOTES"},
        ],
    }
    election = schema.load(raw)
    assert all(isinstance(col, Column) for col in election.subgroups)


def test_parse_lowell_yaml(lowell):
    assert isinstance(lowell, Place)


def test_raise_for_missing(lowell, geodataframe):
    with pytest.raises(MissingColumnsError):
        lowell.raise_for_missing_columns(geodataframe)


def test_deserializes_population_object(lowell):
    assert isinstance(lowell.population, Population)


def test_data_files_are_valid(data_files):
    for data in data_files():
        assert isinstance(PlaceSchema().load(data), Place)


def test_deserializes_election_object(ma_precincts):
    assert all(isinstance(election, Election) for election in ma_precincts.elections)


def test_summarize_column_returns_json_serializable(geodataframe):
    geodataframe["data"] = 0
    print(geodataframe["data"].dtype)
    column = Column(key="data", name="Test data")
    assert json.dumps(summarize_column(column, geodataframe))
