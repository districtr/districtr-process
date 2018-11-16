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
    subgroups = fields.List(Column)


class Election:
    def __init__(self, year, race, parties_to_columns):
        self.year = year
        self.race = race
        self.parties_to_columns = parties_to_columns


class ElectionSchema(Schema):
    year = fields.Integer(validate=lambda x: x > 1776 and x <= datetime.now().year)
    race = fields.String()
    parties_to_columns = fields.List(PartyColumn)


class Party(fields.String):
    pass


class Column(fields.String):
    pass


class PartyColumn(Schema):
    party = Party()
    column = Column()


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
