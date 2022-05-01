import marshmallow as ma



class Item(ma.Schema):
    class Meta:
        ordered = True

    studen_oid= ma.fields.Str()
    date=ma.fields.DateTime()
    class_id= ma.fields.Str()