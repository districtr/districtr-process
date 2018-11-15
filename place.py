class Population:
    def __init__(self, total, subgroups=None):
        self.total = total
        if subgroups is None:
            subgroups = []
        self.subgroups = subgroups


class Election:
    def __init__(self, year, race, parties_to_columns):
        self.year = year
        self.race = race
        self.parties_to_columns = parties_to_columns


class Place:
    def __init__(self, id, name, elections, population):
        self.id = id
        self.name = name
        self.elections = elections
        self.population = population
