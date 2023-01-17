import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY')
    REFRESH_TOKEN_SECRET_KEY = os.getenv('REFRESH_TOKEN_SECRET_KEY')
    RESET_PASSWORD_SECRET_KEY = os.getenv('RESET_PASSWORD_SECRET_KEY')
    SECRET_SALT = f'{os.getenv("SECRET_SALT")}'.encode()

    ACCESS_TOKEN_EXPIRE_TIME = 10  # days
    REFRESH_TOKEN_EXPIRE_TIME = 60  # minutes
    RESET_PASSWORD_TOKEN_EXPIRE_TIME = 20  # minutes

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
    ELASTICSEARCH_USERNAME = os.getenv('ELASTICSEARCH_USERNAME')
    ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')
    ELASTICSEARCH_EVENT_LOGS_INDEX = os.getenv('ELASTICSEARCH_EVENT_LOGS_INDEX')

    ERROR_MESSAGES_PATH = f"{os.path.abspath(os.path.dirname(__file__))}/error_handling/error_messages.json"
    LOGS_FOLDER_PATH = os.getenv('LOGS_FOLDER_PATH')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    LOGS_FOLDER_PATH = os.getenv('LOGS_FOLDER_PATH')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    FLASK_ENV = 'test'
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
