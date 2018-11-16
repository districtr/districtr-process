from datetime import datetime

from marshmallow import Schema, fields


class Population:
    def __init__(self, total, subgroups=None):
        self.total = total
        if subgroups is None:
            subgroups = []
        self.subgroups = subgroups


class PopulationSchema(Schema):
    total = fields.String()
    subgroups = fields.List(ColumnSchema)


class Election:
    def __init__(self, year, race, vote_totals):
        self.year = year
        self.race = race
        self.vote_totals = vote_totals


class ElectionSchema(Schema):
    year = fields.Integer(validate=lambda x: x > 1776 and x <= datetime.now().year)
    race = fields.String()
    vote_totals = fields.List(ColumnSchema)


class ColumnSchema(Schema):
    name = fields.String()
    key = fields.String()


class Place:
    def __init__(self, id, name, elections, population):
        self.id = id
        self.name = name
        self.elections = elections
        self.population = population


class PlaceSchema(Schema):
    id = fields.String()
    name = fields.String()
    elections = fields.List(ElectionSchema)
    population = fields.List(PopulationSchema)
