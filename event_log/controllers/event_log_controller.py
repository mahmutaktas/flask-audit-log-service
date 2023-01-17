from auth.services import auth_services
from event_log.services import event_log_services
from flask import request, Blueprint
from helpers.auth_helpers import login_required
from helpers.token_helpers import get_data_from_token


EVENT_LOG = Blueprint('EVENT_LOG', __name__)


@EVENT_LOG.post('/add')
@login_required()
def add_event_log(current_user):
    data = request.get_json()

    created_by = current_user["id"]

    return event_log_services.add_event_log(data, created_by)


@EVENT_LOG.post('/add-bulk')
@login_required()
def add_bulk_event_log_by_event_type(current_user):
    data = request.get_json()

    created_by = current_user["id"]

    return event_log_services.add_bulk_event_log_by_event_type(data, created_by)


@EVENT_LOG.get('/<event_log_id>')
@login_required()
def get_event_log_by_id(current_user, event_log_id):

    return event_log_services.get_event_log_by_id(event_log_id)


@EVENT_LOG.post('/query')
@login_required()
def get_event_logs_by_query(current_user):

    data = request.json

    return event_log_services.get_event_logs_by_query(data)
