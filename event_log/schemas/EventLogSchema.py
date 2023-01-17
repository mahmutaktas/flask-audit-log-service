from marshmallow import INCLUDE, fields, validates, ValidationError, validate, Schema
from marshmallow.validate import Length, Range
from event_manager.schemas.EventTypeSchema import EventTypeSchema
from event_manager.schemas.EventTypeFieldSchema import EventTypeFieldSchema


class EventLogSchema(Schema):
    class Meta:
        unknown = INCLUDE

    id = fields.String(dump_only=True)

    event_id = fields.Integer(required=True)
    timestamp = fields.DateTime(required=True)
    ip_address = fields.IPv4(required=True)
    user_id = fields.Integer(required=True)
    url = fields.Url(required=True)
    endpoint = fields.String(required=True)

    # TODO: redisten al
    event_type = fields.Nested(lambda: EventTypeSchema(only=('name', 'service_name')), required=True)
    event_specific_data = fields.Dict(dump_only=True)


event_log_create_schema = EventLogSchema(
    only=[
        "event_id",
        "timestamp",
        "ip_address",
        "user_id",
        "url",
        "endpoint",
        "event_type",
    ])
