import pydash as py_
import hashlib

from src.functions import random_string
from .base import BaseDAO
import src.schemas.user as SchemaUser
import bson
from datetime import datetime

'''
* Index:
    1. ```db.getCollection('user').createIndex( { "email": 1 }, { unique: true } )```
    2. ```db.getCollection('user').createIndex( { "name": 1 }, { unique: true } )```
'''


class UserDAO(BaseDAO):

    def exec_register(self, email, password, name, avatar,phone):
        item = {}
        # print(item)
        item['email'] = email.lower()
        item['avatar'] = avatar
        item['name'] = name
        item['phone']=phone
        item['_password'] = password
        # validate
        item['_password_hash_algorithm'] = 'sha256'
        item['_password_salt'] = random_string()
        item['_password'] = hashlib.pbkdf2_hmac(item['_password_hash_algorithm'], item['_password'].encode('utf-8'),
                                                item['_password_salt'].encode("utf-8"), 100000).hex()
        item = SchemaUser.Item().load(item)
        print(item)
        self.insert(item)
        return item

    def get_by_email_password(self, email, password):
        user = self.get_item_with({"email": email})
        if user and self.check_password(user, password):
            return user

        return None

    def check_password(self, user, password):
        if not py_.get(user, '_password'):
            return False
        return py_.get(user, '_password') == hashlib.pbkdf2_hmac(py_.get(user, '_password_hash_algorithm'), password.encode("utf-8"),
                                                                 py_.get(user, '_password_salt').encode("utf-8"), 100000).hex()


    def get_me(self, info):
        user_info = SchemaUser.ItemResponse().dump(info)
        return user_info

    def change_password(self, user_id, new_password):
        now= datetime.now()
        try:
            nowstr = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        except:
            nowstr = now.strftime("%Y-%m-%dT%H:%M:%S")
        item = {}
        item['_password'] = str(new_password)
        item['_password_hash_algorithm'] = 'sha256'
        item['_password_salt'] = random_string()
        item['_password'] = hashlib.pbkdf2_hmac(item['_password_hash_algorithm'], item['_password'].encode('utf-8'),
                                                item['_password_salt'].encode("utf-8"), 100000).hex()
        item['date_change_password']=nowstr

        item = SchemaUser.ItemNewPassword().load(item)
        self.update(bson.ObjectId(user_id),item)
        return 
