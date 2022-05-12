import marshmallow as ma



class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute="_id")

    email = ma.fields.Email()
    avatar = ma.fields.Str()
    name = ma.fields.Str()
    phone = ma.fields.Str()

    _password = ma.fields.Str()
    _password_salt = ma.fields.Str()
    _password_hash_algorithm = ma.fields.Str()




class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    avatar = ma.fields.Str(allow_none=True)
    name = ma.fields.Str(allow_none=True)
    phone = ma.fields.Str(allow_none=True)

class ItemRegister(ma.Schema):
    class Meta:
        ordered = True

    email = ma.fields.Email()
    avatar = ma.fields.Str()
    phone= ma.fields.Str()
    name = ma.fields.Str()
    password = ma.fields.Str(attribute="_password")

class ItemLogin(ma.Schema):
    class Meta:
        ordered = True

    email = ma.fields.Str()
    password = ma.fields.Str(attribute="password")

class ItemResponse(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    id = ma.fields.Str(attribute="_id", )
    email = ma.fields.Email(attribute="email")
    avatar = ma.fields.Str(attribute="avatar")
    name = ma.fields.Str(attribute="name")
    phone = ma.fields.Str()



class ItemNewPassword(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    _password = ma.fields.Str()
    _password_salt = ma.fields.Str()
    _password_hash_algorithm = ma.fields.Str()
    date_change_password = ma.fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%f")

class ItemAuthPassword(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    email = ma.fields.Email()
    current_password = ma.fields.Str()
    new_password = ma.fields.Str()

class ItemSendOTP(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    email = ma.fields.Email()
class ItemCheckOTP(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    email = ma.fields.Email()
    otp= ma.fields.Str()

class ItemResetPassword(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    email = ma.fields.Email()
    otp= ma.fields.Str()
    new_password= ma.fields.Str()