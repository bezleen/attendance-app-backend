import bson
import pydash as py_
import src.models.repo as Repo
import src.schemas.student as SchemaStudent
import src.schemas.images as SchemaImages


class Student(object):

    @classmethod
    def insert_student(cls, user_id, class_id, payload):

        # insert student
        obj = SchemaStudent.Item().load(payload)
        py_.set_(obj, "created_by", user_id)
        #check index
        info=Repo.mStudent.get_item_with(
            {
                "student_id": py_.get(obj, "student_id"), 
                "created_by": py_.get(obj, "created_by")
            }
        )
        if info:
            raise ValueError("Student is already taken!")

        student = Repo.mStudent.insert(obj)
        # append into class
        info=Repo.mStudent.get_item_with(
            {
                "student_id": py_.get(student, "student_id"), 
                "created_by": py_.get(student, "created_by")
            }
        )
        id=py_.get(info,"_id")
        Repo.mClassroom.update_raw(
            {
                "_id": bson.ObjectId(class_id)
            },
            {
                "$set": {},
                "$push": {"student_oid": str(id)}
            }
        )
        # create student_images
        item_images = {
            "student_oid": str(id)
        }
        obj_images = SchemaImages.Item().load(item_images)
        image_id = Repo.mImages.insert(obj_images)
        return str(id)

    @classmethod
    def list_students(cls, user_id, page, page_size):
        list_item = Repo.mStudent.get_list(
            {"created_by": user_id}, page=page, page_size=page_size)
        obj = SchemaStudent.ItemResponse(many=True).dump(list_item)
        return obj

    @classmethod
    def one_student(cls, id):
        item = Repo.mStudent.get_item(id)
        obj = SchemaStudent.ItemResponse().dump(item)
        return obj
    @classmethod
    def one_student_id(cls, id,user_id):
        item = Repo.mStudent.get_item_with(
            {
                "student_id":id,
                "created_by":user_id
            }
            )
        obj = SchemaStudent.ItemResponse().dump(item)
        return obj