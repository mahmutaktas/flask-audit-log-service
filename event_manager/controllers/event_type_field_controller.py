from auth.services import auth_services
from event_manager.services import event_type_field_services
from flask import request, Blueprint
from helpers.auth_helpers import login_required
from helpers.token_helpers import get_data_from_token


EVENT_TYPE_FIELD = Blueprint('EVENT_TYPE_FIELD', __name__)


@EVENT_TYPE_FIELD.post('/create')
@login_required()
def create_event_type_field(current_user):
    data = request.get_json()

    data["created_by"] = current_user["id"]

    return event_type_field_services.create_event_type_field(data)


@EVENT_TYPE_FIELD.post('/update')
@login_required()
def update_event_type_field(current_user):
    data = request.get_json()

    data["updated_by"] = current_user["id"]

    return event_type_field_services.update_event_type(data)


@EVENT_TYPE_FIELD.get('/by-event-type/<event_type_id>')
@login_required()
def get_event_type_fields_by_event_type_id(current_user, event_type_id):

    return event_type_field_services.get_event_type_fields_by_event_type_id(event_type_id)


@EVENT_TYPE_FIELD.get('/field-types')
@login_required()
def get_field_types(current_user):

    return event_type_field_services.get_field_types()
