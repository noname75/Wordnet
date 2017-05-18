from blog.models.db_config import *

class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.Unicode(100), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    moreInfo = db.Column(db.Unicode(1000))