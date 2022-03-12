from logging import NullHandler
from flask_restful import Resource
from flask import request, redirect, make_response, url_for, session, jsonify
import jwt
import datetime
import re

from pymysql import NULL
from db_models.plugins import get_one_plugin, set_plugin_token
from db_models.users import UserModel
from tools.string_tools import gettext
from http import HTTPStatus as hs

from tools.token_tool import authorize



class PluginCrud(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']
    
    @authorize
    def post(self, current_user: UserModel):
        req_data = request.json
        param1 = NULL
        param2 = NULL
        param3 = NULL
        p_name = ''
        try:
            param1 = req_data["param1"]
        except:
            return {"message": gettext("plugin_params_needed")}, hs.BAD_REQUEST
        try:
            param2 = req_data["param2"]
        except:
            pass  
        try:
            param3 = req_data["param3"]
        except:
            pass
        try:
            p_name = req_data["p_name"]
        except:
            return {"message": gettext("plugin_name_needed")}, hs.BAD_REQUEST

        plugin = get_one_plugin(p_name , -1 , self.engine)
        if plugin == None :
            return {"message": gettext("plugin_not_found")}, hs.NOT_FOUND

        set_plugin_token(plugin , current_user , self.engine , param1 , param2 , param3)

        return {"message": gettext("plugin_params_changed")}, hs.OK
      

