import marshmallow as ma



class Item(ma.Schema):
    class Meta:
        ordered = True

    student_oid=ma.fields.Str()
    images=ma.fields.List(ma.fields.Str(),default=[])
    