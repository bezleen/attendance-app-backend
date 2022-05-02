import bson
import pydash as py_
import src.models.repo as Repo
import src.schemas.classroom as SchemaClassroom
import src.constants as Consts
from datetime import datetime, timedelta


class Classroom(object):
    @classmethod
    def list_classroom(cls, user_id, page, page_size):
        list_item = Repo.mClassroom.get_list(
            {"created_by": user_id}, page=page, page_size=page_size)
        obj = SchemaClassroom.ItemResponse(many=True).dump(list_item)
        return obj

    @classmethod
    def add_classroom(cls, user_id, payload):
        obj = SchemaClassroom.Item().load(payload)
        py_.set_(obj, "created_by", user_id)
        info=Repo.mClassroom.get_item_with(
            {
                "name": py_.get(obj, "name"), 
                "created_by": py_.get(obj, "created_by")
            }
        )
        if info:
            raise ValueError("Classroom is already taken!")
        id = Repo.mClassroom.insert(obj)
        return id

    @classmethod
    def add_student(cls, class_id, payload):
        data = py_.get(payload, "student_oid")
        if type(data) == type("bezleendtrbodoi"):
            Repo.mClassroom.update_raw(
                {
                    "_id": bson.ObjectId(class_id)
                },
                {
                    "$set": {},
                    "$push": {"student_oid": data}
                }
            )
        elif type(data) == type([1, 2, 3]):
            Repo.mClassroom.update_raw(
                {
                    "_id": bson.ObjectId(class_id)
                },
                {
                    "$set": {},
                    "$push": {"student_oid": {"$each": data}}
                }
            )
        else:
            raise ValueError("data must be string or list")
        return

    @classmethod
    def list_students(cls, class_id, page, page_size, state, date):
        if state == Consts.STATE_ALL:
            classroom = Repo.mClassroom.get_item(class_id)
            list_student = py_.get(classroom, "student_oid")
            list_info_student = []
            for i in list_student:
                student = Repo.mStudent.get_item(i)
                list_info_student.append(student)
            obj = SchemaClassroom.Student(many=True).dump(list_info_student)

        elif state == Consts.STATE_ABSENT:
            classroom = Repo.mClassroom.get_item(class_id)
            list_student = py_.get(classroom, "student_oid")
            list_info_student = []
            for i in list_student:
                date_start = datetime.strptime(date, Consts.DATETIME_FORMAT)
                date_end = date_start+timedelta(days=1)
                check = Repo.mSheet.get_item_with(
                    {
                        "student_oid": i,
                        "class_id": class_id,
                        "date_created": {"$gte": date_start},
                        "date_created": {"$lt": date_end}
                    }
                )
                if not check:
                    student = Repo.mStudent.get_item(i)
                    list_info_student.append(student)
            obj = SchemaClassroom.Student(many=True).dump(list_info_student)
        elif state == Consts.STATE_ATTENDANCE:
            classroom = Repo.mClassroom.get_item(class_id)
            list_student = py_.get(classroom, "student_oid")
            list_info_student = []
            for i in list_student:
                date_start = datetime.strptime(date, Consts.DATETIME_FORMAT)
                date_end = date_start+timedelta(days=1)
                check = Repo.mSheet.get_item_with(
                    {
                        "student_oid": i,
                        "class_id": class_id,
                        "date_created": {"$gte": date_start},
                        "date_created": {"$lt": date_end}
                    }
                )
                if check:
                    student = Repo.mStudent.get_item(i)
                    list_info_student.append(student)
            obj = SchemaClassroom.Student(many=True).dump(list_info_student)
        return obj


    @classmethod
    def kick_student(cls, class_id, payload):
        data = py_.get(payload, "student_oid")
        if type(data) == type("bezleendtrbodoi"):
            Repo.mClassroom.update_raw(
                {
                    "_id": bson.ObjectId(class_id)
                },
                {
                    "$set": {},
                    "$pull": {"student_oid": data}
                }
            )
        elif type(data) == type([1, 2, 3]):
            Repo.mClassroom.update_raw(
                {
                    "_id": bson.ObjectId(class_id)
                },
                {
                    "$set": {},
                    "$pull": {"student_oid": {"$in": data}}
                }
            )
        else:
            raise ValueError("data must be string or list")
        return