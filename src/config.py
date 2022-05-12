# -*- coding: utf-8 -*-

import os
import json
import datetime
import src.constants as Consts
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
    
    REDIS_USERS_STARTUP_NODES = load_json(os.getenv('REDIS_USERS_STARTUP_NODES', default='[]'))
    MONGO_URI = os.getenv('MONGO_URI')
    UPLOAD_FOLDER = Consts.UPLOAD_FOLDER

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    AT_TIME = int(os.getenv('AT_TIME', 8640000))
    RF_TIME = int(os.getenv('RF_TIME', 3600))
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=AT_TIME)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=RF_TIME)

    FIREBASE_CONFIG = {
        "apiKey": "AIzaSyBBna5KLzdGAlJrsffIFFZf2D_F5ALFL6s",
        "authDomain": "bezleen-app.firebaseapp.com",
        "databaseURL":"https://bezleen-app-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "bezleen-app",
        "storageBucket": "bezleen-app.appspot.com",
        "messagingSenderId": "1061161712722",
        "appId": "1:1061161712722:web:359016b4739596fb76b38b",
        "measurementId": "G-FBDJ8DXCJC",
        "serviceAccount": Consts.SERVICE_ACCOUNT_KEY
    }
