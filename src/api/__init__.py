from .user import bp as rest_user
from .sheet import bp as rest_sheet
from .student import bp as rest_student
from .images import bp as rest_images
from .classroom import bp as rest_classroom


DEFAULT_BLUEPRINTS = [
    rest_user,
    rest_student,
    rest_images,
    rest_sheet,
    rest_classroom
]
