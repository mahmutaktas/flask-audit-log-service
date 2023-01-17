from marshmallow import INCLUDE, fields, validates, ValidationError, validate
from marshmallow.validate import Length, Range
from schema import BaseSchema
from event_manager.models import EventTypeField
from event_manager.schemas import EventTypeSchema
from enums.FieldTypeEnums import FieldType


class EventTypeFieldSchema(BaseSchema):
    class Meta:
        model = EventTypeField
        unknown = INCLUDE

    event_type_id = fields.Integer(required=True)
    event_type = fields.Nested(lambda: EventTypeSchema(only=('id', 'name', 'service_name')), dump_only=True)

    field_name = fields.String(required=True, validate=Length(min=1, max=255))
    field_type = fields.String(required=True, validate=Length(min=1, max=255))

    @validates('field_type')
    def validate_start_date(self, value):

        valid_field_types = [member.value for member in FieldType]

        if value not in valid_field_types:
            raise ValidationError("Invalid field type")


event_type_fields_schema = EventTypeFieldSchema(many=True, exclude=["event_type_id", "event_type"])
event_type_field_create_schema = EventTypeFieldSchema()
event_type_field_update_schema = EventTypeFieldSchema(
    only=["event_type_id", "field_name", "field_type"])
