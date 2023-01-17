import json
from config import Config

with open(Config.ERROR_MESSAGES_PATH, encoding='utf-8') as json_file:
    AUTH_ERRORS = json.load(json_file)["AUTH"]


class LoginFailedError(Exception):

    def __init__(self):
        self.message = AUTH_ERRORS["LOGIN_FAILED"]["text"]
        self.code = AUTH_ERRORS["LOGIN_FAILED"]['code']
        self.http_status = 401


class UserAlreadyExistsError(Exception):

    def __init__(self):
        self.message = AUTH_ERRORS["USER_ALREADY_EXISTS"]["text"]
        self.code = AUTH_ERRORS["USER_ALREADY_EXISTS"]['code']
        self.http_status = 400


class UserNotFoundError(Exception):

    def __init__(self):
        self.message = AUTH_ERRORS["USER_NOT_FOUND"]["text"]
        self.code = AUTH_ERRORS["USER_NOT_FOUND"]['code']
        self.http_status = 404

class_names = [
    LoginFailedError, UserAlreadyExistsError, UserNotFoundError
]
