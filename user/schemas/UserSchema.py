from marshmallow import INCLUDE, fields, validates, ValidationError, validate
from marshmallow.validate import Length, Range
from schema import BaseSchema
from user.models import User


class UserSchema(BaseSchema):
    class Meta:
        model = User
        unknown = INCLUDE

    id = fields.Integer(dump_only=True)

    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=Length(min=1, max=255))
    name = fields.String(required=False, validate=Length(min=1, max=255))
    surname = fields.String(required=False, allow_none=True, missing=None, validate=Length(min=1, max=255))


user_schema = UserSchema()
register_user_schema = UserSchema()
