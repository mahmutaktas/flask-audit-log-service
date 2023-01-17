from auth.services import auth_services
from event_manager.services import event_type_services
from flask import request, Blueprint
from helpers.auth_helpers import login_required
from helpers.token_helpers import get_data_from_token


EVENT_TYPE = Blueprint('EVENT_TYPE', __name__)


@EVENT_TYPE.post('/create')
@login_required()
def create_event_type(current_user):
    data = request.get_json()

    data["created_by"] = current_user["id"]

    return event_type_services.create_event_type(data)


@EVENT_TYPE.post('/update/<event_type_id>')
@login_required()
def update_event_type(current_user, event_type_id):
    data = request.get_json()

    data["updated_by"] = current_user["id"]

    return event_type_services.update_event_type(event_type_id, data)
