from marshmallow import INCLUDE, fields, validates, ValidationError, validate
from marshmallow.validate import Length, Range
from schema import BaseSchema
from event_manager.models import EventType


class EventTypeSchema(BaseSchema):
    class Meta:
        model = EventType
        unknown = INCLUDE

    id = fields.Integer(dump_only=True)

    name = fields.String(required=True, validate=Length(min=1, max=255))
    service_name = fields.String(required=True, validate=Length(min=1, max=255))


event_type_create_schema = EventTypeSchema()
event_type_update_schema = EventTypeSchema(only=["name", "service_name"], partial=True)
