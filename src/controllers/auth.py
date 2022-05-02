import bson
import random as rd
import pydash as py_
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
import src.models.repo as Repo
from src.functions import check_allowed_file
from werkzeug.utils import secure_filename
import src.constants as Consts
import os


class Auth(object):

    @classmethod
    def exec_register(cls, email, password, name, avatar, phone):
        Repo.mUser.exec_register(email, password, name, avatar, phone)
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

        user = Repo.mUser.update_by_filter({
            '_id': bson.ObjectId(user_id)
        }, update_data)
        user_info = Repo.mUser.get_item(oid=user_id)
        return user_info

    @classmethod
    def update_password(cls, user_id: str, email: str, current_password: str, new_password: str):
        user = Repo.mUser.get_by_email_password(email, current_password)
        if not user:
            raise ValueError("User not register or wrong password")
        Repo.mUser.change_password(user_id, new_password)
        return True

    @classmethod
    def exec_upload(cls, file, user_id):
        if file.filename == '':
            raise ValueError("No file selected for uploading")
        if file and check_allowed_file(file.filename):
            name = secure_filename(file.filename)
            prefix = "avatar-" + str(user_id)
            true_filename = prefix+'.'+str(name.split('.')[-1])
            path = os.path.join(Consts.UPLOAD_FOLDER, true_filename)
            file.save(path)
        else:
            raise ValueError("File is not allowed")
        # save path
        Repo.mUser.update_raw(
            {
                "_id":bson.ObjectId(user_id)
            },
            {
                "$set":{"avatar":"/static/uploads/"+true_filename}
            }
        )
        return
