from blog.models.db_config import *

class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(100), unique=True)
    language = db.Column(db.Enum('فارسی', 'انگلیسی', 'عربی','سایر زبان‌ها'))
    moreInfo = db.Column(db.Unicode(1000))