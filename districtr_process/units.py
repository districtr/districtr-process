import warnings

from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf

from .exceptions import MissingColumnsError
from .column_set import ColumnSetSchema
from .columns import IdColumnSchema, NameColumnSchema


class Units:
    """A set of units with which you might draw a districting plan."""

    def __init__(
        self,
        id,
        name=None,
        unit_type=None,
        column_sets=None,
        id_column=None,
        name_column=None,
        source=None,
        bounds=None,
    ):
        if id_column is None:
            warnings.warn('ID column is None for place "{}" ({})'.format(name, id))

        self.id = id

        if name is None:
            name = unit_types[unit_type]
        self.name = name

        self.id_column = id_column
        self.name_column = name_column
        self.unit_type = unit_type
        self.source = source
        self.bounds = bounds

        if column_sets is None:
            column_sets = []
        self.column_sets = column_sets

        assert len(set(column.key for column in self.columns)) == len(
            self.columns
        ), "No duplicate columns are allowed"

    @property
    def columns(self):
        columns = [column for column_set in self.column_sets for column in column_set]

        if self.id_column is not None:
            columns += [self.id_column]

        if self.name_column is not None:
            columns += [self.name_column]

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
        return "<Units id={} name={}>".format(self.id, self.name)

    def record(self, df=None):
        record = {
            "id": self.id,
            "name": self.name,
            "unitType": unit_types[self.unit_type],
            "columnSets": [column_set.record(df) for column_set in self.column_sets],
        }

        if self.id_column is not None:
            record["idColumn"] = self.id_column.record()
        if self.name_column is not None:
            record["nameColumn"] = self.name_column.record()
        if self.bounds is not None:
            record["bounds"] = self.bounds
        elif df is not None:
            record["bounds"] = bounds(df)

        return record

    def keys(self, df):
        id_column = df[self.id_column.key]
        return list(id_column)


def bounds(df):
    """Give [[minx, miny], [maxx, maxy]] for a GeoDataFrame"""
    # Convert minx, miny, maxx, maxy to [[minx, miny], [maxx, maxy]]
    array = [round(n, 4) for n in df.geometry.total_bounds]
    return [[array[0], array[1]], [array[2], array[3]]]


unit_types = {
    "precinct": "Precincts",
    "block": "Blocks",
    "block_group": "Block Groups",
    "county": "Counties",
    "town": "Towns",
    "community_area": "Community Areas",
    "ward": "Wards",
}


def missing_columns(df, columns):
    missing = []
    for column in columns:
        if column.key not in df.columns:
            missing.append(column)
    return missing


class UnitsSchema(Schema):
    id = fields.String(required=True)
    name = fields.String()
    source = fields.String(required=True)
    unit_type = fields.String(validate=OneOf(list(unit_types)))
    column_sets = fields.Nested(ColumnSetSchema, many=True)
    id_column = fields.Nested(IdColumnSchema)
    name_column = fields.Nested(NameColumnSchema)
    bounds = fields.List(fields.List(fields.Float()))

    @post_load
    def create_unit_set(self, data, **kwargs):
        return Units(**data)
