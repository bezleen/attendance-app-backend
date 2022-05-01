import hashlib
import json
import random
import string
import sentry_sdk
import traceback
from marshmallow import pre_load, fields, post_load

from flask import request
from datetime import datetime, date, timedelta


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
        traceback.print_exc()
        sentry_sdk.capture_exception()
    return {}

