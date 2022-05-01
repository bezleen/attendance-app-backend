import bson
import pydash as py_
import src.models.repo as Repo
import src.schemas.student as SchemaStudent


class Student(object):

    @classmethod
    def insert_student(cls, payload):
        # append into class
        class_id = py_.get(payload, "class_id")
        # code here

        # insert student
        obj = SchemaStudent.Item().load(payload)
        id = Repo.mStudent.insert(obj)
        return id

    @classmethod
    def list_students(cls, page, page_size):
        list_item = Repo.mStudent.get_list(page=page, page_size=page_size)
        obj= SchemaStudent.ItemResponse(many=True).dump(list_item)
        return obj
