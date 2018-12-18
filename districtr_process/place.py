import warnings
from datetime import datetime

from marshmallow import Schema, fields, post_load, validate

from .columns import IdColumnSchema, PopulationColumnSchema, VoteColumnSchema
from .exceptions import MissingColumnsError


class Population:
    """Population data, optionally with demographic subgroups"""

    def __init__(self, total, subgroups=None):
        self.total = total
        if subgroups is None:
            subgroups = []
        self.subgroups = subgroups

    @property
    def columns(self):
        return [self.total] + self.subgroups

    def record(self, df=None):
        return {
            "total": summarize_column(self.total, df),
            "subgroups": [
                summarize_column(subgroup, df) for subgroup in self.subgroups
            ],
        }


def summarize_column(column, df=None):
    if df is not None:
        return {"key": column.key, "name": column.name, "sum": df[column.key].sum()}
    else:
        return {"key": column.key, "name": column.name}


class PopulationSchema(Schema):
    total = fields.Nested(PopulationColumnSchema, required=True)
    subgroups = fields.Nested(PopulationColumnSchema, many=True)

    @post_load
    def create_population(self, data):
        return Population(**data)


class Election:
    """Election data"""

    def __init__(self, year, race, vote_totals):
        self.year = year
        self.race = race
        self.vote_totals = vote_totals

    @property
    def columns(self):
        return self.vote_totals

    def __repr__(self):
        return "<Election {} {}>".format(self.year, self.race)

    def __str__(self):
        return "{year} {race} election".format(year=self.year, race=self.race)

    def record(self):
        return {
            "year": self.year,
            "race": self.race,
            "voteTotals": [
                {"key": column.key, "name": column.name} for column in self.vote_totals
            ],
        }


class ElectionSchema(Schema):
    year = fields.Integer(
        validate=validate.Range(min=1776, max=datetime.now().year), required=True
    )
    race = fields.String(required=True)
    vote_totals = fields.Nested(VoteColumnSchema, many=True)

    @post_load
    def make_election(self, data):
        return Election(**data)


class Place:
    """A place where you might draw a districting plan."""

    def __init__(self, id, name, population=None, elections=None, id_column=None):
        if population is None:
            warnings.warn('Population is None for place "{}" ({})'.format(name, id))
        if id_column is None:
            warnings.warn('ID column is None for place "{}" ({})'.format(name, id))

        self.id = id
        self.name = name
        self.population = population
        self.id_column = id_column

        if elections is not None:
            self.elections = elections
        else:
            self.elections = []

    @property
    def columns(self):
        columns = [column for election in self.elections for column in election.columns]

        if self.population is not None:
            columns += self.population.columns

        if self.id_column is not None:
            columns += [self.id_column]

        return columns

    def problems(self, df):
        return {column.key: column.problems(df) for column in self.columns}

    def raise_for_problems(self, df):
        problems = self.problems(df)
        for failures in problems.values():
            if len(failures) > 0:
                raise ValueError(
                    "The given DataFrame is not compatible with {}".format(self),
                    problems,
                )

    def raise_for_missing_columns(self, df):
        """Assert that the given DataFrame has the necessary columns"""
        missing = missing_columns(df, self.columns)
        if len(missing) > 0:
            raise MissingColumnsError(missing)

    def __repr__(self):
        return "<Place id={} name={}>".format(self.id, self.name)

    def record(self, df=None):
        record = {
            "id": self.id,
            "name": self.name,
            "tilesets": tileset_records(self),
            "population": self.population.record(df),
            "elections": [election.record() for election in self.elections],
        }

        if self.id_column is not None:
            record["idColumn"] = self.id_column.record()
        if df is not None:
            record["bounds"] = bounds(df)

        return record


def bounds(df):
    """Give [[minx, miny], [maxx, maxy]] for a GeoDataFrame"""
    # Convert minx, miny, maxx, maxy to [[minx, miny], [maxx, maxy]]
    array = [round(n, 4) for n in df.geometry.total_bounds]
    return [[array[0], array[1]], [array[2], array[3]]]


def tileset_records(place):
    return [
        {
            "type": "fill",
            "source": {
                "type": "vector",
                "url": "mapbox://districtr.{}".format(place.id),
            },
            "sourceLayer": place.id,
        },
        {
            "type": "circle",
            "source": {
                "type": "vector",
                "url": "mapbox://districtr.{}".format(place.id + "_points"),
            },
            "sourceLayer": place.id + "_points",
        },
    ]


def missing_columns(df, columns):
    missing = []
    for column in columns:
        if column.key not in df.columns:
            missing.append(column)
    return missing


class PlaceSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    elections = fields.Nested(ElectionSchema, many=True)
    population = fields.Nested(PopulationSchema)
    id_column = fields.Nested(IdColumnSchema)

    @post_load
    def create_place(self, data):
        return Place(**data)
