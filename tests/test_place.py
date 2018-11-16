import json
import pathlib

import pytest
import yaml

from districtr_process.columns import Column
from districtr_process.exceptions import MissingColumnsError
from districtr_process.place import (
    Election,
    ElectionSchema,
    Place,
    PlaceSchema,
    Population,
)


@pytest.fixture
def lowell():
    with open("data/lowell.yml") as f:
        lowell_yaml = yaml.safe_load(f)
    return PlaceSchema().load(lowell_yaml)


@pytest.fixture
def ma_precincts():
    with open("data/ma-precincts.yml") as f:
        ma_yaml = yaml.safe_load(f)
    return PlaceSchema().load(ma_yaml)


@pytest.fixture
def data_files():
    def generator():
        for filename in pathlib.Path("data").iterdir():
            with open(filename) as f:
                if filename.suffix in ("yml", "yaml"):
                    yield yaml.safe_load(f)
                if filename.suffix == "json":
                    yield json.load(f)

    return generator


def test_lists_of_columns_deserialize():
    schema = ElectionSchema()
    raw = {
        "year": 2000,
        "race": "Presidential",
        "vote_totals": [
            {"name": "Republican", "key": "R_VOTES"},
            {"name": "Democratic", "key": "D_VOTES"},
        ],
    }
    election = schema.load(raw)
    assert all(isinstance(col, Column) for col in election.vote_totals)


def test_parse_lowell_yaml(lowell):
    assert isinstance(lowell, Place)


def test_raise_for_missing(lowell, geodataframe):
    with pytest.raises(MissingColumnsError):
        lowell.raise_for_missing_columns(geodataframe)


def test_deserializes_population_object(lowell):
    assert isinstance(lowell.population, Population)


def test_deserializes_population_object(lowell):
    assert isinstance(lowell.population, Population)


def test_data_files_are_valid(data_files):
    for data in data_files():
        assert isinstance(PlaceSchema().load(data), Place)


def test_deserializes_election_object(ma_precincts):
    assert all(isinstance(election, Election) for election in ma_precincts.elections)
