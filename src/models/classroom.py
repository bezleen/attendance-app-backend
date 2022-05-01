from .base import BaseDAO
import src.schemas.classroom as SchemaClassroom
import bson
from datetime import datetime
import pydash as py_

'''
* Index:
    1. ```db.getCollection('classroom').createIndex( { "name": 1 }, { unique: true } )```
'''

class ClassroomDAO(BaseDAO):
    '''
    '''