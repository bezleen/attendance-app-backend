import bson
import pydash as py_
import src.models.repo as Repo
import src.schemas.sheet as SchemaSheet

class Sheet(object):

    @classmethod
    def roll_call(cls,payload):
        obj= SchemaSheet.Item().load(payload)
        Repo.mSheet.insert(obj) 
        return True
