from blog.models.db_config import *

class Graph(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(200))
    isDirect = db.Column(db.Boolean)
    isActive = db.Column(db.Boolean, default=True)
    language = db.Column(db.Enum('فارسی', 'انگلیسی', 'عربی', 'همه‌ی زبان‌ها'))
    source = db.Column(db.Enum('tags', 'responses', 'tagsAndResponses'))
    minWeight = db.Column(db.Float, default=0)
    minFrequency = db.Column(db.Float, default=0)
    startTime = db.Column(db.DateTime)
    finishTime = db.Column(db.DateTime)
    creationTime = db.Column(db.DateTime())


    def getGraphList_bySource(self, source):
        return db.session.query(Graph).filter_by(source=source).all()