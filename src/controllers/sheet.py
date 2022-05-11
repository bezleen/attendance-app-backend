import bson
import pydash as py_
import src.models.repo as Repo
import src.schemas.sheet as SchemaSheet

class Sheet(object):

    @classmethod
    def roll_call(cls,payload,user_id):
        obj= SchemaSheet.Item().load(payload)
        student_oid=py_.get(obj, "student_oid")
        class_id=py_.get(obj, "class_id")
        check_in_class=Repo.mClassroom.get_item_with(
            {
                "_id":bson.ObjectId(class_id),
                "student_oid":student_oid,
                "created_by":user_id
            }
            )
        if not check_in_class:
            raise ValueError("Student not in class")
        Repo.mSheet.insert(obj) 
        return True
