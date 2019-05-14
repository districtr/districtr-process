from marshmallow import Schema, fields
from marshmallow.validate import Range, OneOf


class DistrictingProblemSchema(Schema):
    name = fields.Str(required=True)
    numberOfParts = fields.Int(validate=Range(min=0))
    pluralNoun = fields.Str()
    type = fields.Str(validate=OneOf(["multimember", "districts", "community"]))
    units = fields.List(fields.Str())
