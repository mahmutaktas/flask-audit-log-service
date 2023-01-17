import json
from config import Config

with open(Config.ERROR_MESSAGES_PATH, encoding='utf-8') as json_file:
    EVENT_MANAGER_ERRORS = json.load(json_file)["EVENT_MANAGER"]


class EventTypeAlreadyExistsError(Exception):

    def __init__(self):
        self.message = EVENT_MANAGER_ERRORS["EVENT_TYPE_ALREADY_EXISTS"]["text"]
        self.code = EVENT_MANAGER_ERRORS["EVENT_TYPE_ALREADY_EXISTS"]['code']
        self.http_status = 400


class EventTypeNotFoundError(Exception):

    def __init__(self):
        self.message = EVENT_MANAGER_ERRORS["EVENT_TYPE_NOT_FOUND"]["text"]
        self.code = EVENT_MANAGER_ERRORS["EVENT_TYPE_NOT_FOUND"]['code']
        self.http_status = 404


class EventTypeFieldAlreadyExistsError(Exception):

    def __init__(self):
        self.message = EVENT_MANAGER_ERRORS["EVENT_TYPE_FIELD_ALREADY_EXISTS"]["text"]
        self.code = EVENT_MANAGER_ERRORS["EVENT_TYPE_FIELD_ALREADY_EXISTS"]['code']
        self.http_status = 400


class EventTypeFieldNotFoundError(Exception):

    def __init__(self):
        self.message = EVENT_MANAGER_ERRORS["EVENT_TYPE_FIELD_NOT_FOUND"]["text"]
        self.code = EVENT_MANAGER_ERRORS["EVENT_TYPE_FIELD_NOT_FOUND"]['code']
        self.http_status = 404


class_names = [
    EventTypeAlreadyExistsError,
    EventTypeNotFoundError,
    EventTypeFieldAlreadyExistsError,
    EventTypeFieldNotFoundError]
