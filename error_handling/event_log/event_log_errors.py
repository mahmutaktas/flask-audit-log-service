import json
from config import Config

with open(Config.ERROR_MESSAGES_PATH, encoding='utf-8') as json_file:
    EVENT_LOG_ERRORS = json.load(json_file)["EVENT_LOG"]


class EitherLessOrMoreFieldError(Exception):

    def __init__(self):
        self.message = EVENT_LOG_ERRORS["EITHER_LESS_OR_MORE_FIELD"]["text"]
        self.code = EVENT_LOG_ERRORS["EITHER_LESS_OR_MORE_FIELD"]['code']
        self.http_status = 400


class_names = [
    EitherLessOrMoreFieldError
]
