USER_DATA = {
    "email": "testuser2@gmail.com",
    "password": "123456",
    "name": "Mahmut",
    "surname": "AKTAŞ",
}

EVENT_TYPE_DATA = {
    "name": "add-cart",
    "service_name": "purchase"
}

EVENT_TYPE_FIELD_DATA = {
    "event_type_id": 1,
    "field_name": "surname",
    "field_type": "String"
}

EVENT_LOG_DATA = {
    "event_id": 1,
    "timestamp": "2022-10-24 23:01:07.634",
    "ip_address": "10.34.53.15",
    "user_id": 12,
    "url": "http://google.com",
    "endpoint": "search?q=smt222",
    "event_type": {
        "name": "register",
        "service_name": "user-profile"
    },
    "username": "mahmutaktas4",
    "register_date": "2022-10-25 22:53:44.830"
}

BULK_EVENT_LOG_DATA = {
    "event_type": {
        "name": "register",
        "service_name": "user-profile"
    },
    "logs": [
        {
            "event_id": 1,
            "timestamp": "2022-10-24 23:01:07.634",
            "ip_address": "111.34.53.15",
            "user_id": 12,
            "url": "http://google.com",
            "endpoint": "search?q=smt222",
            "username": "mahmutaktas4",
            "register_date": "2022-10-25 22:53:44.830",
            "event_type": {
                "name": "register",
                "service_name": "user-profile"
            }
        },
        {
            "event_id": 1,
            "timestamp": "2022-10-24 23:01:07.634",
            "ip_address": "111.34.53.15",
            "user_id": 12,
            "url": "http://google.com",
            "endpoint": "search?q=smt222",
            "username": "mahmutaktas4",
            "register_date": "2022-10-25 22:53:44.830",
            "event_type": {
                "name": "register",
                "service_name": "user-profile"
            }
        },
        {
            "event_id": 1,
            "timestamp": "2022-10-24 23:01:07.634",
            "ip_address": "111.34.53.15",
            "user_id": 12,
            "url": "http://google.com",
            "endpoint": "search?q=smt222",
            "username": "mahmutaktas4",
            "register_date": "2022-10-25 22:53:44.830",
            "event_type": {
                "name": "register",
                "service_name": "user-profile"
            }
        },
        {
            "event_id": 1,
            "timestamp": "2022-10-24 23:01:07.634",
            "ip_address": "111.34.53.15",
            "user_id": 12,
            "url": "http://google.com",
            "endpoint": "search?q=smt222",
            "username": "mahmutaktas4",
            "register_date": "2022-10-25 22:53:44.830",
            "event_type": {
                "name": "register",
                "service_name": "user-profile"
            }
        }
    ]
}


EVENT_LOG_QUERY = {
    "sort": {
        "page": 1,
        "page_size": 20,
        "sort_type": "event_id",
        "sort_dir": "asc"
    },
    "query": {
        "event_specific_data.username": "mahmutaktas"
    }
}
