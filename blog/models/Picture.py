from blog.models.db_config import *

class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(200), unique=True)
    filePath = db.Column(db.Unicode(500))
