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
import src.schemas.student as SchemaStudent
import src.controllers as Controller


bp = Blueprint('student', __name__, url_prefix='/api/student')


@bp.route('', methods=['POST'])
@jwt_required()
def add_student():
    user_id=py_.get(current_user, '_id')
    payload = request.get_json()
    args = request.args
    class_id = py_.get(args, 'class', None)
    try:
        student_id = Controller.Student.insert_student(user_id,class_id, payload)
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
        "data": {"id":student_id},
        "msg": Consts.MESSAGE_SUCCESS
    }

@bp.route('', methods=['GET'])
@jwt_required()
def get_student():
    user_id=py_.get(current_user, '_id')
    args = request.args
    page = py_.to_integer(py_.get(args, 'page', 1))
    page_size = py_.to_integer(py_.get(args, 'page_size', Consts.PAGE_SIZE_MAX))
    try:
        return_data = Controller.Student.list_students(user_id,page,page_size)
    except ValueError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }
    return {
        "status": HTTPStatus.OK,
        "data": return_data,
        "msg": Consts.MESSAGE_SUCCESS
    }

@bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_one_student_by_oid(id):
    try:
        return_data = Controller.Student.one_student(id)
    except ValueError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }
    return {
        "status": HTTPStatus.OK,
        "data": return_data,
        "msg": Consts.MESSAGE_SUCCESS
    }

@bp.route('id/<id>', methods=['GET'])
@jwt_required()
def get_one_student_by_id(id):
    user_id = py_.get(current_user, '_id')
    try:
        return_data = Controller.Student.one_student_id(id,user_id)
    except ValueError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }
    return {
        "status": HTTPStatus.OK,
        "data": return_data,
        "msg": Consts.MESSAGE_SUCCESS
    }