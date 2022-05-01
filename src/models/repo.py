from src.extensions import mdb

from .base import BaseDAO
from .user import UserDAO

mUser = UserDAO(mdb.db.user)

