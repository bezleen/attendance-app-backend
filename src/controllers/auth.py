import bson
import random as rd
import pydash as py_
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
import src.models.repo as Repo
from src.extensions import  redis_cluster, auth
from src.functions import check_allowed_file,random_otp,send_otp_mail
from werkzeug.utils import secure_filename
import src.constants as Consts
import os
from datetime import datetime
import src.firebase_admin_func as fa
class Auth(object):

    # @classmethod
    # def exec_register(cls, email, password, name, avatar, phone):
    #     Repo.mUser.exec_register(email, password, name, avatar, phone)
    #     return True


    @classmethod
    def exec_register_firebase(cls, email, password, name):
        # print("exec_register: ", email, password, name, avatar)
        
        user = auth.create_user_with_email_and_password(email, password)
        Repo.mUser.exec_register_firebase(email, name)
        auth.send_email_verification(user['idToken'])
        # add user UID
        auth_info = auth.get_account_info(user['idToken'])
        user_UID = auth_info['users'][0]['localId']
        Repo.mUser.update_raw(
            {
                "email": email,
                "name": name,
            },
            {
                "$set": {"user_uid": user_UID}
            }
        )
        return True



    # @classmethod
    # def exec_login(cls, email, password):
    #     user = Repo.mUser.get_by_email_password(email, password)
    #     if not user:
    #         return None, None
    #     at = create_access_token(identity=str(
    #         user['_id']), fresh=True, additional_claims={'name': user['name']})
    #     rt = create_refresh_token(identity=str(user['_id']))
    #     # TODO: save token log
    #     return at, rt



    @classmethod
    def exec_login_firebase(cls, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except:
            return None, None
        auth_info = auth.get_account_info(user['idToken'])
        if auth_info['users'][0]['emailVerified'] == False:
            raise ValueError("please verify your email address")
        else:
            user_UID = auth_info['users'][0]['localId']
            print(user_UID)
            user_info = Repo.mUser.get_item_with(
                {
                    "user_uid": user_UID,
                }
            )
            print(user_info)
            name_user = py_.get(user_info, 'name')
            user_oid = py_.get(user_info, '_id')
            at = create_access_token(
                identity=str(user_oid),
                fresh=True,
                additional_claims={
                    'name': name_user
                }
            )
            rt = create_refresh_token(identity=str(user_oid))
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

    @classmethod
    def send_otp(cls, email):
        # print(email)
        # check email address
        info = Repo.mUser.get_item_with({"email": email})
        if not info:
            raise ValueError("email id not valid")
        otp = random_otp(Consts.LENGTH_OTP)
        # send mail
        # print(otp)
        mail_status= send_otp_mail(email,otp)
        if mail_status == False:
            raise ValueError("Email failed")
        # setex otp->redis
        oid = str(py_.get(info, "_id"))
        key = Consts.KEY_OTP_REDIS+oid
        redis_cluster.setex(key, Consts.EXP_OTP, otp)
        return True

    @classmethod
    def check_otp(cls, email, otp):
        # check email address
        info = Repo.mUser.get_item_with({"email": email})
        if not info:
            raise ValueError("email id not valid")
        # get true otp
        oid = str(py_.get(info, "_id"))
        key = Consts.KEY_OTP_REDIS+oid
        true_otp = redis_cluster.get(key)
        if not true_otp:
            raise ValueError("OTP already expired")
        try:
            int_otp = int(otp)
        except:
            raise ValueError("Wrong format OTP")
        if int_otp == int(true_otp):
            # 2 minutes to change password
            redis_cluster.setex(key, Consts.EXP_OTP, true_otp)
            return True
        return False

    @classmethod
    def reset_password(cls, email, otp, new_password):
        # check email address
        info = Repo.mUser.get_item_with({"email": email})
        if not info:
            raise ValueError("email id not valid")
        # get true otp
        oid = str(py_.get(info, "_id"))
        key = Consts.KEY_OTP_REDIS+oid
        true_otp = redis_cluster.get(key)
        if not true_otp:
            raise ValueError("Time already expired")
        try:
            int_otp = int(otp)
        except:
            raise ValueError("Wrong format OTP")
        if int_otp == int(true_otp):
            uid = py_.get(info, 'user_uid')
            result = fa.change_password(uid, new_password)
            if result == False:
                raise ValueError("Change password failed")
            #add date_change_password
            now = datetime.now()
            Repo.mUser.update_raw(
                {
                    "user_uid":uid
                },
                {
                    "$set":{"date_change_password":now}
                }
            )
        return True
