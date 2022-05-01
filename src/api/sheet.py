from http import HTTPStatus
from flask import (
    Blueprint,
    request
)
from marshmallow import ValidationError
import pydash as py_
from pymongo.errors import DuplicateKeyError
from flask_jwt_extended import jwt_required, current_user
import src.constants as Consts
import src.schemas.sheet as SchemaSheet
import src.controllers as Controller


bp = Blueprint('sheet', __name__, url_prefix='/api/sheet')


@bp.route('', methods=['POST'])
@jwt_required()
def attendance():
    payload = request.get_json()
    try:
        Controller.Sheet.roll_call(payload)
    except ValidationError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }
    except ValueError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }
    return {
        "status": HTTPStatus.OK,
        "data": {},
        "msg": Consts.MESSAGE_SUCCESS
    }