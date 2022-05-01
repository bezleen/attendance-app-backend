from .user import bp as rest_user
from .sheet import bp as rest_sheet
from .student import bp as rest_student
from .images import bp as rest_images


DEFAULT_BLUEPRINTS = [
    rest_user,
    rest_student,
    rest_images,
    rest_sheet
]
