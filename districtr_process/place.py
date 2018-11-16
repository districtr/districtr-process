from datetime import datetime
from uuid import uuid4

from marshmallow import Schema, fields, post_load, validate


def missing_columns(df, columns):
    missing = []
    for column in columns:
        if column.key not in df.columns:
            missing.append(column)
    return missing


class Column:
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __repr__(self):
        return "<Column name={} key={}>".format(self.name, self.key)


class ColumnSchema(Schema):
    name = fields.String(required=True)
    key = fields.String(required=True)

    @post_load
    def make_column(self, data):
        return Column(**data)


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


class PopulationSchema(Schema):
    total = fields.Nested(ColumnSchema, required=True)
    subgroups = fields.Nested(ColumnSchema, many=True)


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


class ElectionSchema(Schema):
    year = fields.Integer(
        validate=validate.Range(min=1776, max=datetime.now().year), required=True
    )
    race = fields.String(required=True)
    vote_totals = fields.Nested(ColumnSchema, many=True)

    @post_load
    def make_election(self, data):
        return Election(**data)


class Place:
    """A place where you might draw a districting plan."""

    def __init__(self, id, name, population, elections=None, id_column=None):
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
        return (
            [column for column in election.columns for election in self.elections]
            + [self.id_column]
            + self.population.columns
        )

    def raise_for_missing_columns(self, df):
        """Assert that the given DataFrame has the necessary columns"""
        missing = missing_columns(df, self.columns)
        if len(missing) > 0:
            raise MissingColumnsError(missing)


class MissingColumnsError(Exception):
    pass


class PlaceSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    elections = fields.Nested(ElectionSchema, many=True)
    population = fields.Nested(PopulationSchema)
    id_column = fields.Nested(ColumnSchema)

    @post_load
    def create_place(self, data):
        return Place(**data)
