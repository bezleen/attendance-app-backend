from .base import BaseDAO
import src.schemas.student as SchemaStudent
import bson
from datetime import datetime
import pydash as py_


'''
* Index:
    1. ```db.getCollection('student').createIndex( { "student_id": 1 }, { unique: true } )```
    2. ```db.getCollection('student').createIndex( { "email": 1 }, { unique: true } )
'''

class StudentDAO(BaseDAO):
    '''
    '''