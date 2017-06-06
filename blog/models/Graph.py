from blog.models.db_config import *

class Graph(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.Enum('tags', 'responses'))
    startTime = db.Column(db.DateTime())
    finishTime = db.Column(db.DateTime())
    minUserOnNode = db.Column(db.Integer, default=0)
    minUserOnEdge = db.Column(db.Integer, default=0)
    isDirect = db.Column(db.Boolean)
    minEdgeWeight = db.Column(db.Float, default=0)
    name = db.Column(db.Unicode(50))
    moreInfo = db.Column(db.Unicode(150))
    creationTime = db.Column(db.DateTime())
    isActive = db.Column(db.Boolean, default=True)


    def getGraphList_bySource(self, source):
        return db.session.query(Graph).filter_by(source=source).all()