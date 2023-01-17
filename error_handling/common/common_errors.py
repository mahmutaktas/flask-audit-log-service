import json
from config import Config

with open(Config.ERROR_MESSAGES_PATH, encoding='utf-8') as json_file:
    COMMON_ERRORS = json.load(json_file)["COMMON"]


class UnexpectedErrorOccuredError(Exception):

    def __init__(self):
        self.message = COMMON_ERRORS["UNEXPECTED_ERROR_OCCURED"]["text"]
        self.code = COMMON_ERRORS["UNEXPECTED_ERROR_OCCURED"]['code']
        self.http_status = 500


class TokenNotFoundError(Exception):

    def __init__(self):
        self.message = COMMON_ERRORS["TOKEN_NOT_FOUND"]["text"]
        self.code = COMMON_ERRORS["TOKEN_NOT_FOUND"]['code']
        self.http_status = 401


class InvalidTokenError(Exception):

    def __init__(self):
        self.message = COMMON_ERRORS["INVALID_TOKEN"]["text"]
        self.code = COMMON_ERRORS["INVALID_TOKEN"]['code']
        self.http_status = 401



class_names = [
    UnexpectedErrorOccuredError,
    TokenNotFoundError,
    InvalidTokenError
]
