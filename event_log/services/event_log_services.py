from this import d
from elasticsearch import Elasticsearch
from config import Config
from event_log.schemas.EventLogSchema import event_log_create_schema, EventLogSchema
from event_manager.services import event_type_services, event_type_field_services
from marshmallow import fields, Schema
from enums.FieldTypeEnums import FieldType
from helpers import marshmallow_helpers
from error_handling.event_log import event_log_errors
from error_handling.event_manager import event_manager_errors

ES = Elasticsearch([Config.ELASTICSEARCH_HOST], http_auth=(
    Config.ELASTICSEARCH_USERNAME, Config.ELASTICSEARCH_PASSWORD), verify_certs=False)


def add_event_log(event_log: dict, created_by: int):

    # Validate that does data has all common fields
    errors = event_log_create_schema.validate(event_log)

    if errors:
        return errors

    # Get data's event type
    event_type = event_type_services.get_event_type_exists_by_name_and_service_name(
        event_log["event_type"]["name"], event_log["event_type"]["service_name"])

    if not event_type:
        raise event_manager_errors.EventTypeNotFoundError()

    # Get data's event type fields
    event_type_fields = event_type_field_services.get_event_type_fields_by_event_type_id(event_type.id)["data"]

    # Validate that does data has all event type fields
    incoming_field_count = len(event_log)
    necessary_field_count = len(event_log_create_schema.fields) + len(event_type_fields)

    if incoming_field_count != necessary_field_count:
        raise event_log_errors.EitherLessOrMoreFieldError()

    # We save event type id so even thoug event type name would change, we can group the same logs still
    event_log["event_type"]["id"] = event_type.id
    event_log["created_by"] = created_by

    event_log["event_specific_data"] = {}

    # Validate and append event specific fields
    for event_type_field in event_type_fields:
        field_name = event_type_field["field_name"]
        field_type = event_type_field["field_type"]
        value = event_log[field_name]

        errors = validate_event_specific_data(field_name, field_type, value)

        if errors:
            return errors

        # Append current field into a dict
        event_log["event_specific_data"][field_name] = value
        del event_log[field_name]  # remove the duplicate key value

    ES.index(index=Config.ELASTICSEARCH_EVENT_LOGS_INDEX, document=event_log)

    return {"success": True, "message": "Log succesfully added"}


def add_bulk_event_log_by_event_type(event_logs: list, created_by: int):
    event_type_name = event_logs["event_type"]["name"]
    event_type_service_name = event_logs["event_type"]["service_name"]

    logs = event_logs["logs"]

    # Get data's event type
    event_type = event_type_services.get_event_type_exists_by_name_and_service_name(
        event_type_name, event_type_service_name)

    if not event_type:
        raise event_manager_errors.EventTypeNotFoundError()

    event_type_fields = event_type_field_services.get_event_type_fields_by_event_type_id(event_type.id)["data"]

    event_log_bulk_list = []

    for event_log in logs:
        event_log = prepare_event_log_for_bulking(event_log, event_type, event_type_fields, created_by)
        event_idx = {"index": {"_index": Config.ELASTICSEARCH_EVENT_LOGS_INDEX}}
        event_log_bulk_list.append(event_idx)
        event_log_bulk_list.append(event_log)

    ES.bulk(index=Config.ELASTICSEARCH_EVENT_LOGS_INDEX, body=event_log_bulk_list)

    return {"success": True, "message": "Logs succesfully added"}


def prepare_event_log_for_bulking(event_log: dict, event_type: dict, event_type_fields: list, created_by: int):

    errors = event_log_create_schema.validate(event_log)

    if errors:
        return errors

    # Validate that does data has all event type fields
    incoming_field_count = len(event_log)
    necessary_field_count = len(event_log_create_schema.fields) + len(event_type_fields)

    if incoming_field_count != necessary_field_count:
        raise event_log_errors.EitherLessOrMoreFieldError()

    event_log["event_type"]["id"] = event_type.id
    event_log["created_by"] = created_by
    event_log["event_specific_data"] = {}

    # Validate and append event specific fields
    for event_type_field in event_type_fields:
        field_name = event_type_field["field_name"]
        field_type = event_type_field["field_type"]
        value = event_log[field_name]

        errors = validate_event_specific_data(field_name, field_type, value)

        if errors:
            return errors

        # Append current field into a dict
        event_log["event_specific_data"][field_name] = value
        del event_log[field_name]  # remove the duplicate key value

    return event_log


def get_event_log_by_id(id: str):
    return ES.get(index=Config.ELASTICSEARCH_EVENT_LOGS_INDEX, id=id)["_source"]


def validate_event_specific_data(field_name: str, field_type: str, value: str):
    # Get field type as marshamallow class
    dynamic_schema = marshmallow_helpers.get_dynamic_schema_from_field_name_and_type(field_name, field_type)

    # Validate data
    errors = dynamic_schema.validate({field_name: value})

    return errors


def get_event_logs_by_query(data: dict):
    query_data = data["query"]
    sort_data = data["sort"]

    sort = f"{sort_data['sort_type']}:{sort_data['sort_dir']}"
    page_size = sort_data["page_size"]
    page = sort_data["page"] - 1

    accepted_filter_fields = ["event_id", "ip_address", "user_id", "created_by"]
    accepted_query_fields = ["url", "endpoint"]

    # Initialize elasticsearch fields and queries
    es_filters = []
    es_queries = []

    for search_key, search_val in query_data.items():

        if search_key in accepted_filter_fields:
            if not isinstance(search_val, list):
                search_val = [search_val]  # this allows querying for multiple values
            es_filters.append(
                {"terms": {search_key: search_val}})

        elif search_key in accepted_query_fields:
            es_queries.append(
                {"match_phrase_prefix": {search_key: search_val}})
        elif "event_specific_data" in search_key:
            es_queries.append(
                {"match_phrase_prefix": {search_key: search_val}})

    if len(es_queries) <= 0 and len(es_filters) <= 0:
        return {"count": 0, "data": []}

    query = {
        "bool": {
            "must": es_queries,
            "filter": es_filters
        }
    }

    result = ES.search(
        index=Config.ELASTICSEARCH_EVENT_LOGS_INDEX,
        query=query,
        sort=sort,
        from_=page * page_size,
        size=page_size,
        track_total_hits=True,
        request_timeout=30)

    count = result.body["hits"]["total"]["value"]
    logs = [log["_source"] for log in result.body["hits"]["hits"]]

    return {"count": count, "data": logs}
