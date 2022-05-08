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




    def __init__(self, user_id, data , name):
        self.user_id = user_id
        self.data = data
        self.name = name

    @property
    def json(self):
        dic = {
               "id": self.id,
               "user_id": self.user_id,
               "data": self.data
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
    
def get_user_sketch(user_id, engine):
    session = make_session(engine)
    our_user = session.query(SketchModel).filter(SketchModel.user_id == user_id ).all()
    return our_user

def get_user_sketch_by_name(user_id,name ,engine):
    session = make_session(engine)
    our_user = session.query(SketchModel).filter(db.and_(SketchModel.user_id == user_id  , SketchModel.name == name)).first()
    return our_user