from flask import Blueprint, jsonify, request as flask_request
from error_handling.auth import auth_errors
from error_handling.common import common_errors
from error_handling.event_log import event_log_errors
from error_handling.event_manager import event_manager_errors
import logging
import sys
from config import DevConfig


error_page = Blueprint('error_page', __name__, template_folder="templates")

STREAM_FORMATTER = logging.Formatter(
    '[%(asctime)s] : %(name)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d')

FILE_FORMATTER = logging.Formatter(
    '[%(asctime)s] : %(name)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : %(url)s : %(user_id)s : %(data)s')


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(STREAM_FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = logging.FileHandler(f'{DevConfig.LOGS_FOLDER_PATH}/error_logs.log')
    file_handler.setFormatter(FILE_FORMATTER)
    file_handler.setLevel(logging.ERROR)
    return file_handler


error_file_handler = get_file_handler()

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

# Write logs to both console and file
log.addHandler(get_console_handler())
log.addHandler(error_file_handler)


def handle_custom_error(error):
    from helpers import auth_helpers, token_helpers
    from user.services import user_services

    payload = dict()
    payload['message'] = error.message
    payload['code'] = error.code
    if hasattr(error, 'data'):
        payload['data'] = error.data

    if hasattr(error, 'exception_object') and error.exception_object is not None:

        current_user = {"id": None}

        rcv_token = auth_helpers.get_token_from_request()

        if rcv_token:
            response = token_helpers.get_data_from_token(rcv_token)

            if response:
                email = response["email"]

                user = user_services.get_user_by_email(email)
                current_user["id"] = user["id"] if user else None

        request_info = {
            "url": flask_request.url,
            "user_id": current_user["id"],
            "data": flask_request.get_json() if flask_request.get_data() else {}
        }
        log.error(error.exception_object, exc_info=True, extra=request_info)
    return jsonify(payload), error.http_status


def register_all_error_handlers(app):
    # Register all custom exception classes to the app
    for class_name in auth_errors.class_names:
        app.register_error_handler(class_name, handle_custom_error)

    for class_name in common_errors.class_names:
        app.register_error_handler(class_name, handle_custom_error)

    for class_name in event_log_errors.class_names:
        app.register_error_handler(class_name, handle_custom_error)

    for class_name in event_manager_errors.class_names:
        app.register_error_handler(class_name, handle_custom_error)
