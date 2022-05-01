import bson
import random as rd
import pydash as py_
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
import src.models.repo as Repo




class Auth(object):

    @classmethod
    def exec_register(cls, email, password, name, avatar,phone):
        Repo.mUser.exec_register(email, password, name, avatar,phone)
        return True

    @classmethod
    def exec_login(cls, email, password):
        user = Repo.mUser.get_by_email_password(email, password)
        if not user:
            return None, None
        at = create_access_token(identity=str(
            user['_id']), fresh=True, additional_claims={'name': user['name']})
        rt = create_refresh_token(identity=str(user['_id']))
        # TODO: save token log
        return at, rt

    @classmethod
    def update_info(cls, user_id: str,  update_data: dict):
        user_info = Repo.mUser.get_item(oid=user_id)
        if 'show_skin' in update_data:
            user_skins = py_.get(user_info, 'skins')
            if not update_data['show_skin'] in user_skins:
                raise ValueError('user_not_owned_skin')

        user = Repo.mUser.update_by_filter({
            '_id': bson.ObjectId(user_id)
        }, update_data)
        return {
            **user_info,
            **update_data
        }


    @classmethod
    def update_password(cls, user_id: str,email: str,current_password: str,new_password: str):
        user = Repo.mUser.get_by_email_password(email, current_password)
        if not user:
            raise ValueError("User not register or wrong password")
        Repo.mUser.change_password(user_id,new_password)
        return True