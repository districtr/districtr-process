from marshmallow import Schema, fields, pre_load
from marshmallow.validate import OneOf

from .districting_problems import DistrictingProblemSchema
from .states import states
from .units import UnitsSchema


class PlaceSchema(Schema):
    id = fields.String(required=True)
    name = fields.Str(required=True)
    state = fields.Str(validate=OneOf(states))
    description = fields.Str()
    units = fields.Nested(UnitsSchema, many=True)
    districtingProblems = fields.Nested(DistrictingProblemSchema, many=True)
    landmarks = fields.Dict()

    @pre_load
    def rename(self, data):
        if "districting_problems" in data:
            data["districtingProblems"] = data["districting_problems"]
            del data["districting_problems"]
        return data
