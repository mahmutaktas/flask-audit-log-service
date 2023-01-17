from marshmallow import Schema, fields, INCLUDE


class BaseSchema(Schema):

    created_by = fields.Integer(required=False)
    created_date = fields.DateTime(dump_only=True)

    updated_by = fields.Integer(required=False)
    updated_date = fields.DateTime(dump_only=True)
