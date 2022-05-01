from src.extensions import mdb

from .base import BaseDAO
from .user import UserDAO
from .sheet import SheetDAO
from .student import StudentDAO
from .images import ImagesDAO
from .classroom import ClassroomDAO

mUser = UserDAO(mdb.db.user)
mSheet = SheetDAO(mdb.db.sheet)
mStudent = StudentDAO(mdb.db.student)
mImages=ImagesDAO(mdb.db.images)
mClassroom = ClassroomDAO(mdb.db.classroom)