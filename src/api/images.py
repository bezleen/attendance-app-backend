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
import src.schemas.images as SchemaImages
import src.controllers as Controller


bp = Blueprint('images', __name__, url_prefix='/api/images')


@bp.route('', methods=['GET'])
@jwt_required()
def get_images():
    args = request.args
    page = py_.to_integer(py_.get(args, 'page', 1))
    page_size = py_.to_integer(py_.get(args, 'page_size', Consts.PAGE_SIZE_MAX))
    try:
        return_data = Controller.Images.list_images(page,page_size)
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
def upload_file():
    args = request.args
    student_oid = py_.get(args, 'student_oid', None)
    try:
        if 'file' not in request.files:
            return{
                "status": HTTPStatus.BAD_REQUEST,
                "data": {},
                "msg": "No file part in the request"
            }
        file = request.files['file']
        return_data = Controller.Images.exec_upload(file,student_oid)
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