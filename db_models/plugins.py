from typing import List
import sqlalchemy as db
from db_models.users import UserModel
from tools.db_tool import make_session, Base
from tools.crypt_tool import app_bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import re
import datetime

changed_s = "{} changed successfully"


class PluginModel(Base):
    __tablename__ = "Plugins"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_name = db.Column(db.VARCHAR(150), nullable=True , unique=True)
    params = db.Column(db.VARCHAR(150), nullable=False)
    link = db.Column(db.VARCHAR(150), nullable=False)
    description = db.Column(db.VARCHAR(150))
    image = db.Column(db.VARCHAR(150), nullable=True)


    def __init__(self, p_name, params, link ,description ,  image):

        self.p_name = p_name
        self.params = params
        self.link = link
        self.description = description
        self.image = image

    @property
    def json(self):
        dic = {"p_name": self.p_name,
               "params": self.params,
               "link": self.link,
               "description": self.description,
               "image": self.image,
               }
        return dic

def init_plugins(engine):
    session = make_session(engine)
    plugin_lists = [
    {
        'p_name':'whois',
        'params':'token',
        'link':'whoisxmlapi.com',
        'description':'',
        'image':'pluginp/whois.png'
    }
    ]
    for row in plugin_lists:
        try:
            jwk_user = PluginModel(p_name=row['p_name'], params=row['params'], link=row['link'] ,description=row['description'] , image=row['image'] )
            session.add(jwk_user)
            session.commit()
        except:
            pass







def add_plugin(p_name, params, link,description,image, engine):
    session = make_session(engine)
    jwk_user = PluginModel(p_name, params, link,description,image)
    session.add(jwk_user)
    session.commit()

def get_one_plugin(p_name, id, engine):
    session = make_session(engine)
    our_user = session.query(PluginModel).filter((PluginModel.p_name == p_name) | (PluginModel.id == id)).first()
    return our_user


class PluginCrudModel(Base):
    __tablename__ = "PluginCrud"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_name = db.Column(db.VARCHAR(150), nullable=False)
    user_id = db.Column(db.VARCHAR(150), nullable=False)
    plugin_id = db.Column(db.VARCHAR(150), nullable=False)
    param1 = db.Column(db.VARCHAR(150), nullable=True)
    param2 = db.Column(db.VARCHAR(150), nullable=True)
    param3 = db.Column(db.VARCHAR(150), nullable=True)



    def __init__(self, p_name, user_id, plugin_id ,param1 ,  param2 , param3):
        self.p_name = p_name
        self.user_id = user_id
        self.plugin_id = plugin_id
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    @property
    def json(self):
        dic = {"p_name": self.p_name,
               "user_id": self.user_id,
               "plugin_id": self.plugin_id,
               "param1": self.param1,
               "param2": self.param2,
               'param3':self.param3
               }
        return dic

def get_one_plugin_crud(plugin_id, user_id, engine):
    session = make_session(engine)
    our_user = session.query(PluginCrudModel).filter(db.and_(PluginCrudModel.plugin_id == plugin_id) , (PluginCrudModel.user_id == user_id)).first()
    return our_user

def set_plugin_token(plugin: PluginModel,user: UserModel, engine , param1 , param2=db.null , param3=db.null):
    session = make_session(engine)
    crud = get_one_plugin_crud(plugin.id , user.id , engine)
    if crud == None:
        jwk_user = PluginCrudModel(p_name=plugin.p_name, user_id=user.id, plugin_id=plugin.id ,param1=param1 , param2=param2 , param3=param3 )
        session.add(jwk_user)
    else:
        session.query(PluginCrudModel).filter(PluginCrudModel.id == crud.id).update({PluginCrudModel.param1: param1 ,
        PluginCrudModel.param2: param2 , PluginCrudModel.param3: param3})
        session.flush()
    session.commit()
    