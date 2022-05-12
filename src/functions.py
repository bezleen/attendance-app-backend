
import json
import random
import string
import src.constants as Consts

from flask import request
from datetime import datetime, date, timedelta
import smtplib


def json_decode_hook(obj):
    if '__datetime__' in obj:
        return datetime.strptime(obj['as_str'], "%Y%m%dT%H:%M:%S.%f")
    if b'__datetime__' in obj:
        return datetime.strptime(obj[b'as_str'], "%Y%m%dT%H:%M:%S.%f")
    return obj



def random_string():
    """Generate a random string with the combination of lowercase and uppercase letters """
    string_length = random.randint(10, 15)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))

def load_json(string: str):
    try:
        return json.loads(string, object_hook=json_decode_hook)
    except:
        pass
    return {}
def check_allowed_file(filename):
    tail = filename.split('.')[-1].lower() 
    if '.' in filename and tail in Consts.ALLOWED_FILE:
        return True
    return False
def random_otp(length):
    otp=''
    for i in range(7):
        num = random.randint(0,9)
        otp=otp+str(num)
    return otp
def send_otp_mail(email,otp):
    try:
        sender_email = "19520532@gm.uit.edu.vn"
        rec_email = email
        password = Consts.SMTP_PASSWORD
        message = 'Subject: "OTP Confirmation"\n\nThis is your OTP: {}'.format(otp)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        print("Login smtp success")
        server.sendmail(sender_email, rec_email, message)
        print("Email has been sent to ", rec_email)
        return True
    except:
        return False

