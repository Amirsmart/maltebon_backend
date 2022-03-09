from typing import List
import sqlalchemy as db
from tools.db_tool import make_session, Base
from tools.crypt_tool import app_bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import re
import datetime

changed_s = "{} changed successfully"


class PluginModel(Base):
    __tablename__ = "Users"
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
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_name = db.Column(db.VARCHAR(150), nullable=False)
    user_id = db.Column(db.VARCHAR(150), nullable=False)
    plugin_id = db.Column(db.VARCHAR(150), nullable=False)
    param1 = db.Column(db.VARCHAR(150), nullable=True)
    param2 = db.Column(db.VARCHAR(150), nullable=True)
    param3 = db.Column(db.VARCHAR(150), nullable=True)



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