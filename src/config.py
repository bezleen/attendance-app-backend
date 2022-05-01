# -*- coding: utf-8 -*-

import os
import json
import datetime
from dotenv import load_dotenv
from src.functions import load_json

load_dotenv()


class BaseConfig(object):
    PROJECT = "bezleen-api"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = "bezleendtrbodoi"


class DefaultConfig(BaseConfig):
    DEBUG = True

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    MONGO_URI = os.getenv('MONGO_URI')



    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    AT_TIME = int(os.getenv('AT_TIME', 8640000))
    RF_TIME = int(os.getenv('RF_TIME', 3600))
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=AT_TIME)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=RF_TIME)

