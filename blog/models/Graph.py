from blog.models.db_config import *

class Graph(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isDirect = db.Column(db.Boolean)
    isActive = db.Column(db.Boolean, default=True)
    language = db.Column(db.Enum('فارسی', 'انگلیسی', 'عربی', 'همه‌ی زبان‌ها'))
    source = db.Column(db.Enum('پاسخ‌های کاربران سایت', 'تگ‌های اینستاگرام', 'تگ‌های اینستاگرام و پاسخ‌های کاربران سایت'))
    minWeight = db.Column(db.Float, default=0)
    minFrequency = db.Column(db.Float, default=0)
    startTime = db.Column(db.DateTime)
    finishTime = db.Column(db.DateTime)