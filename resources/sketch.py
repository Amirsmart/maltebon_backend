from flask_restful import Resource
from flask import request, make_response, jsonify


from pymysql import NULL
from db_models.sketch import add_sketch, get_user_sketch_by_name, get_user_sketchs 
from db_models.users import UserModel
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