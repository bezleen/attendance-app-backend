import marshmallow as ma



class Item(ma.Schema):
    class Meta:
        ordered = True

    name=ma.fields.Str()
    student_id=ma.fields.Str()
    email= ma.fields.Email()

class ItemResponse(ma.Schema):
    class Meta:
        ordered = True

    id= ma.fields.Str(attribute="_id")
    name=ma.fields.Str()
    student_id=ma.fields.Str()
    email= ma.fields.Email()