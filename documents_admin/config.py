from os import getenv
import logging


class Config(object):
    DEBUG = False
    TESTING = False
    HOST = getenv('HOST', '0.0.0.0')
    PORT = getenv('PORT', 80)
    SECRET_KEY = getenv('SECRET_KEY',
                        '41614b7a614b7e11ca6b8948eae76b606e89eb57ef1bfc8a')
    REQUEST_LIFETIME = 30
    LOGLEVEL = logging.ERROR
    DB_URL = 'sqlite:///documents.sqlite'

    # security configuration
    # Flask-Security config
    SECURITY_URL_PREFIX = "/"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    # SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/document/"
    SECURITY_POST_LOGOUT_VIEW = "/"
    SECURITY_POST_REGISTER_VIEW = "/document/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = getenv('PORT', 5000)
    REQUEST_LIFETIME = 0  # don't check against replay attacks
