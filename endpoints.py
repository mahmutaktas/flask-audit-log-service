from auth.controllers.auth_controller import AUTH
from event_manager.controllers.event_type_controller import EVENT_TYPE
from event_manager.controllers.event_type_field_controller import EVENT_TYPE_FIELD
from event_log.controllers.event_log_controller import EVENT_LOG


def register_endpoints(app):
    app.register_blueprint(AUTH, url_prefix='/auth')
    app.register_blueprint(EVENT_TYPE, url_prefix='/event/type')
    app.register_blueprint(EVENT_TYPE_FIELD, url_prefix='/event/type-field')
    app.register_blueprint(EVENT_LOG, url_prefix='/event/log')
