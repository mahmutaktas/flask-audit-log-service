from datetime import timedelta
from http.client import BAD_REQUEST, NOT_FOUND
from io import BytesIO
import traceback
from flask import abort, jsonify, make_response, send_file
from sqlalchemy import and_, asc, desc, func
from config import Config
from user.models import User
from models import db
from helpers.password_helpers import encode_password
from helpers.token_helpers import generate_access_token, get_data_from_token, generate_reset_password_token, hash_token
from user.schemas.UserSchema import register_user_schema
from error_handling.auth import auth_errors
from error_handling.common import common_errors


def is_user_exists_by_email(email: str):
    user = User.query.filter_by(email=email).first()

    return user if user else None


def login(email: str, password: str):

    encoded_password = encode_password(password)

    user = db.session.query(User).filter(
        User.email == email, User.password == encoded_password).first()

    if user:
        access_token = generate_access_token(email)

        return {
            "success": True,
            "message": "User successfully logged in",
            "access_token": access_token
        }

    raise auth_errors.LoginFailedError()


def register(user_data: dict):

    if is_user_exists_by_email(user_data["email"]):
        raise auth_errors.UserAlreadyExistsError()

    errors = register_user_schema.validate(user_data)

    if errors:
        return errors

    try:
        user_data["password"] = encode_password(user_data["password"])

        user = User(**user_data)

        db.session.add(user)
        db.session.commit()

    except BaseException:
        db.session.rollback()
        traceback.print_exc()
        raise common_errors.UnexpectedErrorOccuredError()

    return {"success": True, "message": "User succesfully created"}
