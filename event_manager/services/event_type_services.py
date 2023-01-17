from models import db
from event_manager.models import EventType
from event_manager.schemas.EventTypeSchema import event_type_create_schema, event_type_update_schema
from error_handling.event_manager import event_manager_errors


def is_event_type_exists_by_id(event_type_id: int):
    event_type = EventType.query.filter_by(id=event_type_id).first()

    return event_type if event_type else None


def get_event_type_exists_by_name_and_service_name(name: str, service_name: str):
    event_type = EventType.query.filter_by(name=name, service_name=service_name).first()

    return event_type if event_type else None


def create_event_type(data: dict):

    errors = event_type_create_schema.validate(data)

    if errors:
        return errors

    if get_event_type_exists_by_name_and_service_name(data["name"], data["service_name"]):
        raise event_manager_errors.EventTypeAlreadyExistsError()

    event_type = EventType(**data)

    db.session.add(event_type)
    db.session.commit()

    return {"success": True, "message": "Event type successfully created"}


def update_event_type(event_type_id: int, data: dict):
    event_type = is_event_type_exists_by_id(event_type_id)

    if not event_type:
        raise event_manager_errors.EventTypeNotFoundError()

    errors = event_type_update_schema.validate(data)

    if errors:
        return errors

    for key, value in data.items():
        setattr(event_type, key, value)

    db.session.commit()

    return {"success": True, "message": "Event type successfully updated"}
