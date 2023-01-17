from functools import wraps
from flask import request
from helpers.date_helpers import get_current_datetime_str
from user.services import user_services
from helpers.auth_helpers import get_token_from_request
from helpers.token_helpers import get_data_from_token
from config import Config


def add_action_log(http_status_code):

    if request.url_rule is None or '.' not in request.url_rule.endpoint:
        controller = "app"
        method = ""
    else:
        endpoint = request.url_rule.endpoint.split('.')
        controller = endpoint[0]
        method = endpoint[1]

    rcv_token = get_token_from_request()
    user_id = 0

    if rcv_token:

        response = get_data_from_token(rcv_token)

        if response:
            email = response["email"]

            current_user = user_services.get_user_by_email(email)

            if current_user:
                user_id = current_user["id"]

    data = request.get_json() if request.get_data() else {}

    action_log = f"[{get_current_datetime_str()}] : {http_status_code} : {request.method} : {request.url} : {controller} : {method} : {data} : {user_id} : {request.user_agent.string}"
    action_log_file = open(f"{Config.LOGS_FOLDER_PATH}/action_logs.log", 'a')
    action_log_file.write(action_log + "\n")
    action_log_file.close()

    return
