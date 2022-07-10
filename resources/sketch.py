import os
from flask_restful import Resource
from flask import request, make_response, jsonify


from pymysql import NULL
from db_models.sketch import add_sketch, change_sketch_image, get_user_sketch_by_name, get_user_sketch_by_token, get_user_sketchs 
from db_models.users import UserModel
from tools.image_tool import get_extension
from tools.string_tools import gettext
from http import HTTPStatus as hs

from tools.token_tool import authorize



class Sketch(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']
    
    @authorize
    def post(self, current_user: UserModel):
        req_data = request.json
        name = NULL
        data = NULL
        try:
            name = req_data["name"]
        except:
            return {"message": gettext("sketch_name_needed")}, hs.BAD_REQUEST
        try:
            data = req_data["data"]
        except:
            return {"message": gettext("sketch_data_needed")}, hs.BAD_REQUEST

        check = get_user_sketch_by_name(current_user.id , name , self.engine)
        if check is not None:
            return {'message':gettext("sketch_already_exist")},401
        sketch = add_sketch(current_user , self.engine , data , name)

        return {"message": gettext("sketch_added") , 'res':sketch}, hs.OK
     
    @authorize
    def get(self, current_user: UserModel):
        data = []
        res = get_user_sketchs(current_user.id  , self.engine)
        for d in res:
            data.append(d.json)
        return make_response(jsonify(data, 200))
    
    @authorize
    def patch(self, current_user: UserModel):
        req_data = request.json
        name = NULL
        try:
            name = req_data["name"]
        except:
            return {"message": gettext("sketch_name_needed")}, hs.BAD_REQUEST

        res = get_user_sketch_by_name(current_user.id , name , self.engine)
        if res is None:
            return {"message": gettext("sketch_not_found") }, 404
        res = res.json
        return make_response(jsonify(res, 200))
    
    @authorize
    def put(self, current_user: UserModel):
        req_data = request.json
        token = NULL
        try:
            token = req_data["token"]
        except:
            return {"message": gettext("sketch_token_needed")}, hs.BAD_REQUEST

        res = get_user_sketch_by_token(current_user.id , token , self.engine)
        if res is None:
            return {"message": gettext("sketch_not_found") }, 404
        res = res.json
        return make_response(jsonify(res, 200))

class sketch_picture(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']

    @authorize
    def post(self, current_user):
        """insert or change current user profile picture"""
        req_data = request.json
        id = NULL
        try:
            id = req_data["id"]
        except:
            return {"message": gettext("sketch_id_needed")}, hs.BAD_REQUEST
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
                os.makedirs(os.getcwd() + gettext('UPLOAD_FOLDER') + '/sp/', exist_ok=True)
            except:
                pass
            url = gettext('UPLOAD_FOLDER') + 'pp/' + str(current_user.id) + get_extension(file.filename)
            try:
                os.remove(url)
            except:
                pass
            file.save(os.getcwd() + url)
            change_sketch_image(current_user,id , url, self.engine)
            return make_response(jsonify(message=gettext("upload_success")), 200)
