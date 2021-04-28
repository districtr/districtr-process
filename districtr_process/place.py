from marshmallow import Schema, fields, EXCLUDE, INCLUDE
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
    districting_problems = fields.Nested(DistrictingProblemSchema, many=True, unknown=INCLUDE)
    landmarks = fields.Dict()
