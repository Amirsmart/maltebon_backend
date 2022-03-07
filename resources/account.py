import os
from flask_restful import Resource
from flask import request, redirect, make_response, url_for, jsonify, render_template
from http import HTTPStatus as hs
import jwt
from sqlalchemy.orm.base import NOT_EXTENSION
from config import jwt_secret_key
from tools.db_tool import engine
from tools.image_tool import get_extension
from tools.mail_tools import send_mail
from tools.token_tool import authorize

from db_models.users import change_user_image, edit_bio, get_notifications, get_one_user, add_user, change_pass, \
    edit_fname, edit_dob, \
    UserModel, delete_expired_notifications, see_notification
from tools.string_tools import gettext
from typing import Union, Dict, Tuple, List


def is_available(req: Dict, *args: List[str]) -> Tuple[bool, str]:
    for s in args:
        t = req.get(s, None)
        if t is None:
            return False, gettext("item_not_found").format(s)

    return True, gettext("item_name_exists").format(s)


class myprofile(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def get(self, current_user: UserModel):
        """:return current user info"""
        res = current_user.json
        return make_response(jsonify(res, 200))

    @authorize
    def post(self, current_user):
        """insert or change current user fname"""
        req_data = request.json
        v = is_available(req_data, "profile_name")
        if not v[0]:
            return make_response(jsonify(v[1], 401))
        edit_fname(current_user, req_data['profile_name'], self.engine)
        return make_response(
            jsonify(message=gettext("item_edited").format("profile name")))  # redirect(url_for("myprofile"))


class fname(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def post(self, current_user):
        """insert or change current user profile_name"""
        req_data = request.json
        v = is_available(req_data, "profile_name")
        if not v[0]:
            return make_response(jsonify(v[1], 401))
        edit_fname(current_user, req_data['profile_name'], self.engine)
        return make_response(
            jsonify(message=gettext("item_edited").format("profile name")))


class bio(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def post(self, current_user):
        """insert or change current user bio"""
        req_data = request.json
        bio_data = req_data.get("bio")
        if bio_data is None:
            return make_response(jsonify(message=gettext("item_not_found").format("bio")), 401)
        edit_bio(current_user, req_data['bio'], self.engine)
        return make_response(jsonify(message=gettext("item_edited").format("bio")), 200)
        # return redirect(url_for("myprofile"))


class dob(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def post(self, current_user):
        """insert or change current user bio"""
        req_data = request.json
        bio_data = req_data.get("dob")
        if bio_data is None:
            return make_response(jsonify(message=gettext("item_not_found").format("dob")), 401)
        edit_dob(current_user, req_data['dob'], self.engine)
        return make_response(jsonify(message=gettext("item_edited").format("dob")), 200)
        # return redirect(url_for("myprofile"))


class profile_picture(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def get(self, current_user: UserModel):
        return make_response(jsonify(url=current_user.image), hs.OK)

    @authorize
    def post(self, current_user):
        """insert or change current user profile picture"""
        files = request.files
        file = files.get('file')
        if 'file' not in request.files:
            return make_response(jsonify(message=gettext("upload_no_file")), 400)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return make_response(jsonify(message=gettext("upload_no_filename")), 400)
        if file:
            try:
                os.makedirs(os.getcwd() + gettext('UPLOAD_FOLDER') + '/pp/', exist_ok=True)
            except:
                pass
            url = gettext('UPLOAD_FOLDER') + 'pp/' + str(current_user.id) + get_extension(file.filename)
            try:
                os.remove(url)
            except:
                pass
            file.save(os.getcwd() + url)
            change_user_image(current_user, url, self.engine)
            return make_response(jsonify(message=gettext("upload_success")), 200)


class password(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def post(self, current_user):
        """change current_user password"""
        req_data = request.json
        res = change_pass(current_user, req_data['old_password'], req_data['new_password'], self.engine)

        if res:
            return make_response(jsonify(message=gettext("item_edited").format("password")), 200)

        else:
            return make_response(jsonify(message=gettext("wrong_pass")), hs.BAD_REQUEST)


class Notifications(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def get(self, current_user: UserModel):
        """:return current user notifications"""
        res = get_notifications(current_user.id, self.engine)
        return make_response(jsonify(res, 200))
    
    @authorize
    def put(self , current_user: UserModel):
        req_data = request.json
        id = -1 
        try:
            id = req_data["id"]
        except:
            return {"message": gettext("notification_id_needed")}, hs.BAD_REQUEST
        res = see_notification(id, self.engine)
        return make_response(jsonify(res, 200))
        

    @authorize
    def delete(self, current_user):
        delete_expired_notifications(self.engine, current_user)
