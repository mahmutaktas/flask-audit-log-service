from auth.services import auth_services
from flask import request, Blueprint

from helpers.token_helpers import get_data_from_token


AUTH = Blueprint('AUTH', __name__)


@AUTH.post('/login')
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    return auth_services.login(email, password)


@AUTH.post('/register')
def register():
    data = request.get_json()

    return auth_services.register(data)
