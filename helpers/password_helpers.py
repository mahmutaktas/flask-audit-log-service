import hashlib
from functools import wraps
import random
import string
from config import Config


def encode_password(password: str):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), Config.SECRET_SALT, 100000).hex()
