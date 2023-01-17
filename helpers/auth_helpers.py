from functools import wraps
from flask import request
from helpers.token_helpers import get_data_from_token
from config import Config
from error_handling.common import common_errors
from error_handling.auth import auth_errors


def login_required(roles=[]):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from user.services import user_services

            rcv_token = get_token_from_request()

            if not rcv_token:
                raise common_errors.TokenNotFoundError()

            response = get_data_from_token(rcv_token)

            if not response:
                raise common_errors.InvalidTokenError()

            email = response["email"]

            current_user = user_services.get_user_by_email(email)

            if not current_user:
                raise auth_errors.UserNotFoundError()

            return f(current_user, *args, **kwargs)

        return decorated

    return decorator


def get_token_from_request():
    rcv_token = None

    token = request.args.get('access-token')

    if token is not None and len(token) > 0:
        rcv_token = token

    if 'access-token' in request.headers:
        rcv_token = request.headers['access-token']

    return rcv_token
