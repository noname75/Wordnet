from blog.models.db_config import *

class Graph(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.Enum('tags', 'responses'))
    startTime = db.Column(db.DateTime())
    finishTime = db.Column(db.DateTime())
    minUserOnNode = db.Column(db.Integer, default=0)
    minUserOnEdge = db.Column(db.Integer, default=0)
    isDirected = db.Column(db.Boolean)
    minEdgeWeight = db.Column(db.Float, default=0)
    name = db.Column(db.Unicode(50))
    moreInfo = db.Column(db.Unicode(150))
    creationTime = db.Column(db.DateTime())
    isActive = db.Column(db.Boolean, default=False)


    def getGraphList_bySource(self, source):
        return db.session.query(Graph).filter_by(source=source).all()


    def __init__(self,
                 source=None,
                 startTime=None,
                 finishTime=None,
                 minUserOnNode=None,
                 minUserOnEdge=None,
                 isDirected=None,
                 minEdgeWeight=None,
                 name=None,
                 moreInfo=None,
                 creationTime=None):
        self.source = source
        self.startTime = startTime
        self.finishTime = finishTime
        self.minUserOnEdge = minUserOnEdge
        self.minUserOnNode = minUserOnNode
        self.minEdgeWeight = minEdgeWeight
        self.isDirected = isDirected
        self.name = name
        self.moreInfo = moreInfo
        self.creationTime = creationTime


    def addGraph(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self