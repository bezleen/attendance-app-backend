from http import HTTPStatus
from flask import (
    Blueprint,
    request
)
from marshmallow import ValidationError
import pydash as py_
from pymongo.errors import DuplicateKeyError
from flask_jwt_extended import jwt_required, current_user,get_jwt_identity


import src.constants as Consts


import src.schemas.user as SchemaUser
import src.controllers as Controller


bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/me', methods=['GET'])
@jwt_required()
def user_info():
    info = SchemaUser.ItemResponse().dump(current_user)
    raw_path_avatar = py_.get(info,"avatar")
    if raw_path_avatar:
        true_path= Consts.PREFIX_CDN + raw_path_avatar
        py_.set_(info,"avatar", true_path)
    return {
        "status": HTTPStatus.OK,
        "data": info,
        "msg": Consts.MESSAGE_SUCCESS
    }


@bp.route('/auth', methods=['POST'])
def auth():
    payload = request.get_json()
    try:
        item = SchemaUser.ItemLogin().load(payload)
        at, rt = Controller.Auth.exec_login(
            item.get('email'), item.get('_password'))

        if not at:
            return {
                "status": HTTPStatus.UNAUTHORIZED,
                "data": {},
                "msg": "User not register or wrong password"
            }
    except ValidationError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }

    return {
        "status": HTTPStatus.OK,
        "data": {
            "access_token": at,
            "refresh_token": rt
        },
        "msg": Consts.MESSAGE_SUCCESS
    }


@bp.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    try:
        item = SchemaUser.ItemRegister().load(payload)
        Controller.Auth.exec_register(item.get('email'), item.get(
            '_password'), item.get('name'), item.get('avatar'),item.get('phone'))
    except ValidationError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }
    except DuplicateKeyError as e:
        return {
            "status": HTTPStatus.NOT_ACCEPTABLE,
            "data": {},
            "msg": "Email or username already taken!"
        }

    return {
        "status": HTTPStatus.OK,
        "data": {},
        "msg": Consts.MESSAGE_SUCCESS
    }


@bp.route('', methods=['PUT'])
@jwt_required()
def update_info():
    payload = request.get_json()
    try:
        user_id = py_.get(current_user, '_id')
        item = SchemaUser.ItemUpdate().load(payload)
        user_info = Controller.Auth.update_info(
            user_id=user_id, update_data=item)
        user_info = SchemaUser.ItemResponse().dump(user_info)
        return {
            "status": HTTPStatus.OK,
            "data": user_info,
            "msg": Consts.MESSAGE_SUCCESS
        }
    except ValueError as e:
        return {
            "status": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": str(e)
        }



@bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    payload = request.get_json()
    user_id = py_.get(current_user, '_id')
    try:
        new_info=SchemaUser.ItemAuthPassword().load(payload)
        email= py_.get(new_info, 'email')
        current_password=py_.get(new_info, 'current_password')
        new_password = py_.get(new_info, 'new_password')
        Controller.Auth.update_password(user_id,email, current_password,new_password)

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


@bp.route('/avatar', methods=['PUT'])
@jwt_required()
def upload_file():
    user_id = py_.get(current_user, '_id')
    try:
        if 'file' not in request.files:
            return{
                "status": HTTPStatus.BAD_REQUEST,
                "data": {},
                "msg": "No file part in the request"
            }
        file = request.files['file']
        return_data = Controller.Auth.exec_upload(file,user_id)
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



@bp.route("/refresh", methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token, refresh_token = Controller.Auth.get_token(
        identity)
    return{
        "status": HTTPStatus.OK,
        "data": {
            "access_token": access_token,
            "refresh_token":refresh_token
        },
        "msg": Consts.MESSAGE_SUCCESS
    }