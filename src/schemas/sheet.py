import marshmallow as ma
from datetime import datetime


class Item(ma.Schema):
    class Meta:
        ordered = True

    student_oid= ma.fields.Str()
    class_id= ma.fields.Str()