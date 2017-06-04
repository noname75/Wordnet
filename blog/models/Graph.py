from blog.models.db_config import *

class Graph(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(200))
    moreInfo = db.Column(db.Unicode(1000))
    isDirect = db.Column(db.Boolean)
    source = db.Column(db.Enum('tags', 'responses', 'tagsAndResponses'))
    minEdgeWeight = db.Column(db.Float, default=0)
    minUserOnNode = db.Column(db.Float, default=0)
    minUserOnEdge = db.Column(db.Float, default=0)
    creationTime = db.Column(db.DateTime())
    isActive = db.Column(db.Boolean, default=True)



    def getGraphList_bySource(self, source):
        return db.session.query(Graph).filter_by(source=source).all()