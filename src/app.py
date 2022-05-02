from flask import Flask
from datetime import datetime
from .config import DefaultConfig
import src.constants as Consts
from .extensions import (
    mdb, jwt
)

# For import *
__all__ = ['create_app']


def create_app(app_name=None):
    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app)
    configure_extensions(app)
    configure_blueprints(app)
    print("upload folder : "+str(Consts.UPLOAD_FOLDER))
    return app


def configure_app(app):
    app.config.from_object(DefaultConfig)


def configure_extensions(app):
    print(app.config['MONGO_URI'])

    # mongodb
    mdb.init_app(app, uri=app.config['MONGO_URI'])

    jwt.init_app(app)

    @jwt.user_lookup_loader
    def load_user(_jwt_header, jwt_data):

        def get_user(user):
            if user:
                user['_id'] = str(user['_id'])
                return user
            return {}

        def check_expired(jwt_data,user):
            iat = jwt_data['iat']
            iat_datetime = datetime.fromtimestamp(iat)
            if 'date_change_password' in user:
                date = user['date_change_password']
                if iat_datetime < date:
                    return 0
            return 1

        from src.models.repo import mUser
        identity = jwt_data["sub"]
        user = mUser.get_item(identity)
        result = check_expired(jwt_data,user)
        if result == 0:
            return None

        user = get_user(user)
        return user


def configure_blueprints(app):
    from src.api import DEFAULT_BLUEPRINTS as blueprints
    for blueprint in blueprints:
        app.register_blueprint(
            blueprint,
            url_prefix=f'/v1/{blueprint.url_prefix}'
        )

