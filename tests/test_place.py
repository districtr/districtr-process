import pytest
import yaml

from districtr_process.columns import Column, MissingColumnsError
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


def test_lists_of_columns_deserialize():
    schema = ElectionSchema()
    raw = {
        "year": 2000,
        "race": "Presidential",
        "vote_totals": [
            {"party": "Republican", "key": "R_VOTES"},
            {"party": "Democratic", "key": "D_VOTES"},
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
