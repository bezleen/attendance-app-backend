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


bp = Blueprint('classroom', __name__, url_prefix='/api/classroom')


@bp.route('', methods=['GET'])
@jwt_required()
def list_all_user_class():
    user_id = py_.get(current_user, '_id')
    args = request.args
    page = py_.to_integer(py_.get(args, 'page', 1))
    page_size = py_.to_integer(
        py_.get(args, 'page_size', Consts.PAGE_SIZE_MAX))
    try:
        return_data = Controller.Classroom.list_classroom(user_id,page, page_size)
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


@bp.route('', methods=['POST'])
@jwt_required()
def add_class():
    user_id = py_.get(current_user, '_id')
    payload = request.get_json()
    try:
        return_data = Controller.Classroom.add_classroom(user_id,payload)
    except ValueError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }
    except DuplicateKeyError as e:
        return {
            "status": HTTPStatus.NOT_ACCEPTABLE,
            "data": {},
            "msg": "Classroom already taken!"
        }
    return {
        "status": HTTPStatus.OK,
        "data": {},
        "msg": Consts.MESSAGE_SUCCESS
    }


@bp.route('/<id>', methods=['PUT'])
@jwt_required()
def add_student_into_class(id):
    payload = request.get_json()
    try:
        Controller.Classroom.add_student(id,payload)
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


@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def kick_student_in_class(id):
    payload = request.get_json()
    try:
        Controller.Classroom.kick_student(id,payload)
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

@bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_list_student(id):
    args = request.args
    page = py_.to_integer(py_.get(args, 'page', 1))
    page_size = py_.to_integer(
        py_.get(args, 'page_size', Consts.PAGE_SIZE_MAX))
    state=py_.get(args, 'state', Consts.STATE_ALL)
    date=py_.get(args, 'date', None)
    try:
        return_data = Controller.Classroom.list_students(id,page,page_size,state,date)
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