import sys
from flask import Flask, request
import os
from dotenv import load_dotenv
from config import DevConfig, ProdConfig, TestConfig, Config
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from error_handling import log, register_all_error_handlers, error_file_handler
from flask.logging import default_handler


app = Flask(__name__, template_folder='templates')


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from models import db
    import models

    load_dotenv()

    if os.getenv("TESTING") == "False":
        if os.getenv("FLASK_DEBUG") == "False":
            app.config.from_object(ProdConfig)
        else:
            app.config.from_object(DevConfig)
    else:
        app.config.from_object(TestConfig)

    db.init_app(app)

    migrate = Migrate(app, db)

    from endpoints import register_endpoints

    register_endpoints(app)

    return app


app = create_app()

register_all_error_handlers(app)


@app.errorhandler(Exception)
def handle_internal_server_error(e):
    from error_handling.common.common_errors import UnexpectedErrorOccuredError, InvalidTokenError
    from helpers.auth_helpers import get_token_from_request
    from helpers.token_helpers import get_data_from_token
    from user.services import user_services
    '''
        Log and return unhandled exceptions in the entire application
    '''

    rcv_token = get_token_from_request()
    user_id = 0

    if rcv_token:

        response = get_data_from_token(rcv_token)

        if response:
            email = response["email"]

            current_user = user_services.get_user_by_email(email)

            if current_user:
                user_id = current_user["id"]

    request_info = {
        "url": request.url,
        "user_id": user_id,
        "data": request.get_json() if request.get_data() else {}
    }
    log.error(e, exc_info=True, extra=request_info)
    unexpected_error = UnexpectedErrorOccuredError()

    return {"code": unexpected_error.code, "message": unexpected_error.message}, UnexpectedErrorOccuredError().http_status


app.logger.removeHandler(default_handler)
app.logger.addHandler(error_file_handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    request_info = {
        "url": '',
        "user_id": 0,
        "data": {}
    }

    log.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback), extra=request_info)


sys.excepthook = handle_exception


@app.after_request
def after_request_func(response):
    from app_logging.action_log import add_action_log

    add_action_log(response.status_code)

    return response


with app.app_context():
    from models import db

    db.create_all()
    db.session.commit()

app.config['CORS_ALLOW_HEADERS'] = '*'
app.config['CORS_ORIGINS'] = '*'
app.config['CORS_SUPPORTS_CREDENTIALS'] = False
app.config['CORS_METHODS'] = ["GET", "HEAD",
                              "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
cors = CORS(app)
ma = Marshmallow(app)


@app.route('/')
def hello_world():
    return 'Hello World!'
