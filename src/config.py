import os
import json
from dotenv import load_dotenv

load_dotenv()

class DefaultConfig(object):
    PROJECT_NAME = "bezleen_api"

    PROJECT_ROOT=""
    DEBUG=True
    TESTING=False
    SECRETKEY="bezleen_dtr_bo_doi"

    BABEL_DEFAULT_LOCALE = 'en'
    MONGO_URI=os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    AT_TIME = int(os.getenv('AT_TIME', 8640000))
    RF_TIME = int(os.getenv('RF_TIME', 3600))
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=AT_TIME)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=RF_TIME)