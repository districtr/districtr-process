import pandas
from marshmallow import Schema, fields, post_load
from pandas.api.types import is_numeric_dtype

from .exceptions import MissingColumnsError


def all_nonnegative(column):
    return (column >= 0).all()


def not_all_zero(column):
    return (column != 0).any()


def has_unique_values(column):
    return len(column) == len(set(column))


class Column:
    tests = []
    require_numeric = None

    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __repr__(self):
        return '<Column name="{}" key={}>'.format(self.name, self.key)

    def problems(self, df):
        failed = []
        if self.key not in df.columns:
            raise MissingColumnsError("Missing column {}".format(self))

        if self.require_numeric is True:
            try:
                df[self.key] = pandas.to_numeric(df[self.key]).round(4).astype(float)
            except Exception:
                failed.append("require_numeric")

        column = df[self.key]

        for assertion in self.tests:
            passed = False
            try:
                passed = assertion(column)
            except Exception:
                passed = False
            if not passed:
                failed.append(assertion.__name__)
        return failed

    def record(self):
        return {"name": self.name, "key": self.key}


class ColumnSchema(Schema):
    name = fields.String(required=True)
    key = fields.String(required=True)


class IdColumn(Column):
    tests = [has_unique_values]


class NameColumn(Column):
    tests = []


class NameColumnSchema(ColumnSchema):
    @post_load
    def make_column(self, data, **kwargs):
        return NameColumn(**data)


class IdColumnSchema(ColumnSchema):
    @post_load
    def make_column(self, data, **kwargs):
        return IdColumn(**data)


class VoteColumn(Column):
    tests = [is_numeric_dtype, all_nonnegative, not_all_zero]
    require_numeric = True


class PopulationColumn(Column):
    tests = [is_numeric_dtype, all_nonnegative, not_all_zero]
    require_numeric = True
