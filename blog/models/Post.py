from blog.models.db_config import *

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Unicode(50), unique=True)
    publishTime = db.Column(db.DateTime)
    storeTime = db.Column(db.DateTime)
    uid = db.Column(db.Integer)