import yaml

from districtr_process.place import Column, Election, ElectionSchema, Place, PlaceSchema


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


def test_parse_lowell_yaml():
    with open("data/lowell.yml") as f:
        raw = yaml.safe_load(f)
    schema = PlaceSchema()
    lowell = schema.load(raw)
    assert isinstance(lowell, Place)
