from .column_types import column_types
from .columns import ColumnSchema
from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf


class ColumnSet:
    """A set of related columns. E.g. a population or election data."""

    def __init__(self, type, name=None, total=None, subgroups=None, metadata=None):
        self.type = type
        self.name = name
        if total is not None:
            self.total = total
        if subgroups is None:
            subgroups = []
        self.subgroups = subgroups
        if metadata is None:
            metadata = dict()
        self.metadata = metadata

    def __repr__(self):
        subgroups_string = ", ".join(subgroup.key for subgroup in self.subgroups)
        return "<{} [{}]>".format(self.__class__.__name__, subgroups_string)

    def __iter__(self):
        return iter(self.columns)

    @property
    def columns(self):
        if not hasattr(self, "total"):
            return self.subgroups
        return [self.total] + self.subgroups

    def record(self, df=None):
        result = {"type": self.type}

        if self.name is not None:
            result["name"] = self.name

        if hasattr(self, "total"):
            result["total"] = summarize_column(self.total, df)

        result["subgroups"] = [
            summarize_column(subgroup, df) for subgroup in self.subgroups
        ]

        if len(self.metadata) > 0:
            result["metadata"] = self.metadata

        return result


def summarize_column(column, df=None):
    if df is not None:
        col_sum = df[column.key].sum()
        col_min = df[column.key].min()
        col_max = df[column.key].max()
        return {
            "key": column.key,
            "name": column.name,
            "sum": int(col_sum),
            "min": int(col_min),
            "max": int(col_max),
        }
    else:
        return {"key": column.key, "name": column.name}


class ColumnSetSchema(Schema):
    type = fields.String(validate=OneOf(list(column_types)), required=True)
    name = fields.String()
    total = fields.Nested(ColumnSchema)
    subgroups = fields.Nested(ColumnSchema, many=True)
    metadata = fields.Dict()

    @post_load
    def create_column_set(self, data):
        ColumnModel = column_types[data["type"]]

        result = {"type": data["type"]}
        if "metadata" in data:
            result["metadata"] = data["metadata"]

        if "name" in data:
            result["name"] = data["name"]

        if "total" in data:
            result["total"] = ColumnModel(**data["total"])

        if "subgroups" in data:
            result["subgroups"] = [
                ColumnModel(**column) for column in data["subgroups"]
            ]
        else:
            result["subgroups"] = []

        return ColumnSet(**result)
