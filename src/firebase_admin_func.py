from firebase_admin import messaging ,auth
import firebase_admin
from firebase_admin import credentials
import os
import src.constants as Consts


cred = credentials.Certificate(Consts.SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)



def change_password(uid, new_password):
    try:
        user = auth.update_user(uid=uid,password=new_password)
    except:
        return False
    return True