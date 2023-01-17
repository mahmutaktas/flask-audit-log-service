import traceback
import jwt
from helpers.date_helpers import get_current_date
from config import Config
from datetime import datetime, timedelta
import hashlib


def generate_access_token(user_email):

    expire_time = Config.ACCESS_TOKEN_EXPIRE_TIME

    try:
        payload = {
            # Token expire time set to day for the sake of simplicity of this task
            'exp': datetime.utcnow() + timedelta(days=expire_time),
            'iat': datetime.utcnow(),
            'email': user_email,
        }
        encoded_token = jwt.encode(
            payload,
            Config.TOKEN_SECRET_KEY,
            algorithm='HS256'
        )
        return encoded_token
    except Exception as e:
        traceback.print_exc()
        return e


def generate_reset_password_token(email):

    expire_time = Config.RESET_PASSWORD_TOKEN_EXPIRE_TIME  # minutes

    try:
        payload = {
            'exp': get_current_date() + timedelta(minutes=expire_time),
            'iat': datetime.utcnow(),
            'email': email,
        }
        encoded_token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm='HS256'
        )
        return encoded_token
    except Exception as e:
        return


def hash_token(token):

    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', token.encode('utf-8'), Config.SECRET_SALT, 100000)

    return hashed_password.hex()


def get_data_from_token(token):
    try:
        data = jwt.decode(str.encode(token),
                          Config.TOKEN_SECRET_KEY, algorithms=['HS256'])

        return {"email": data["email"]}

    except Exception as e:
        return None
