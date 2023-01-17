from models import db
from event_manager.models import EventTypeField
from event_manager.schemas.EventTypeFieldSchema import event_type_fields_schema, event_type_field_create_schema, event_type_field_update_schema
from enums.FieldTypeEnums import FieldType
from event_manager.services import event_type_services
from error_handling.event_manager import event_manager_errors


def is_event_type_field_exists_by_event_type_id_and_field_name(event_type_id: int, field_name: str):
    event_type_field = EventTypeField.query.filter_by(event_type_id=event_type_id, field_name=field_name).first()

    return event_type_field if event_type_field else None


def create_event_type_field(data: dict):

    errors = event_type_field_create_schema.validate(data)

    if errors:
        return errors

    if is_event_type_field_exists_by_event_type_id_and_field_name(data["event_type_id"], data["field_name"]):
        raise event_manager_errors.EventTypeFieldAlreadyExistsError()

    event_type_field = EventTypeField(**data)

    db.session.add(event_type_field)
    db.session.commit()

    return {"success": True, "message": "Event type field successfully created"}


def update_event_type(data: dict):
    errors = event_type_field_update_schema.validate(data)

    if errors:
        return errors

    event_type_field = is_event_type_field_exists_by_event_type_id_and_field_name(
        data["event_type_id"], data["field_name"])

    if not event_type_field:
        raise event_manager_errors.EventTypeFieldNotFoundError()

    accepted_update_columns = ["field_type"]

    for key, value in data.items():
        if key in accepted_update_columns:
            setattr(event_type_field, key, value)

    db.session.commit()

    return {"success": True, "message": "Event type field successfully updated"}


def get_event_type_fields_by_event_type_id(event_type_id: int):
    if not event_type_services.is_event_type_exists_by_id(event_type_id):
        raise event_manager_errors.EventTypeNotFoundError()

    event_type_fields = EventTypeField.query.filter_by(event_type_id=event_type_id).all()

    event_type_fields = event_type_fields_schema.dump(event_type_fields)

    return {"success": True, "data": event_type_fields}


def get_field_types():
    field_types = [member.value for member in FieldType]

    return {"success": True, "data": field_types}
