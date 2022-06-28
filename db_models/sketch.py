from lib2to3.pgen2 import token
from matplotlib import image
from requests import session
import sqlalchemy as db
from db_models.users import UserModel
from tools.db_tool import make_session, Base


import datetime

changed_s = "{} changed successfully"

class SketchModel(Base):
    __tablename__ = "SketchModel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.VARCHAR(150), nullable=False)
    name = db.Column(db.VARCHAR(150), nullable=False)
    data = db.Column(db.TEXT, nullable=True)
    image = db.Column(db.VARCHAR(150), nullable=True)
    token = db.Column(db.VARCHAR(150), nullable=False)
    




    def __init__(self, user_id, data , name ):
        self.user_id = user_id
        self.data = data
        self.name = name
        self.token = str(datetime.datetime.now() ).replace(' ' , '').replace('-','').replace(':','').replace('.','') + name

    @property
    def json(self):
        dic = {
               "id": self.id,
               "user_id": self.user_id,
               "name": self.name,
               "token": self.token,
               "data": self.data,
               "image": self.image
               }
        return dic

def get_one_sketch(id, engine):
    session = make_session(engine)
    our_user = session.query(SketchModel).filter(SketchModel.id == id ).first()
    return our_user



def add_sketch(user: UserModel, engine , data , name):
    session = make_session(engine)
    jwk_user = SketchModel(user_id=user.id, data=data , name=name )
    session.add(jwk_user)
    session.commit()
    return jwk_user.json
    
def get_user_sketchs(user_id, engine):
    session = make_session(engine)
    print("[DEBUG]1")
    our_user = session.query(SketchModel).filter(SketchModel.user_id == user_id ).all()
    print("[DEBUG]2")
    return our_user

def get_user_sketch_by_name(user_id,name ,engine):
    session = make_session(engine)
    our_user = session.query(SketchModel).filter(db.and_(SketchModel.user_id == user_id  , SketchModel.name == name)).first()
    return our_user

def get_user_sketch_by_token(user_id,token ,engine):
    session = make_session(engine)
    our_user = session.query(SketchModel).filter(db.and_(SketchModel.user_id == user_id  , SketchModel.token == token)).first()
    return our_user

def change_sketch_image(current_user: UserModel,sketch_id, url, engine):
    session = make_session(engine)
    session.query(SketchModel).filter(db.and_(SketchModel.user_id == current_user.id,SketchModel.id == sketch_id) ).update({SketchModel.image: url})
    session.flush()
    session.commit()
    return changed_s.format("image"), 200