from marshmallow import Schema, fields, post_load
from pandas.api.types import is_numeric_dtype


def all_nonnegative(column):
    return (column >= 0).all()


def not_all_zero(column):
    return (column != 0).any()


class MissingColumnsError(Exception):
    pass


class Column:
    tests = []

    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __repr__(self):
        return "<Column name={} key={}>".format(self.name, self.key)

    def problems(self, df):
        failed = []
        if self.key not in df.columns:
            raise MissingColumnsError("Missing column {}".format(self))

        column = df[self.key]

        for assertion in self.tests:
            if not assertition(column):
                failed.append(assertion.__name__)
        return failed


class ColumnSchema(Schema):
    name = fields.String(required=True)
    key = fields.String(required=True)

    @post_load
    def make_column(self, data):
        return Column(**data)


class VoteColumn(Column):
    tests = [is_numeric_dtype, all_nonnegative, not_all_zero]


class VoteColumnSchema(ColumnSchema):
    @post_load
    def make_column(self, data):
        return VoteColumn(**data)


class PopulationColumn(Column):
    tests = [is_numeric_dtype, all_nonnegative, not_all_zero]


class PopulationColumnSchema(ColumnSchema):
    @post_load
    def make_column(self, data):
        return PopulationColumn(**data)
