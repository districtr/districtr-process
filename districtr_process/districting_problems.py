from marshmallow import Schema, fields
from marshmallow.validate import Range, OneOf


class DistrictingProblemSchema(Schema):
    name = fields.Str(required=True)
    number_of_parts = fields.Int(validate=Range(min=0))
    plural_noun = fields.Str()
    type = fields.Str(
        validate=OneOf(["multimember", "districts", "community"]), default="districts"
    )
    units = fields.List(fields.Str())
