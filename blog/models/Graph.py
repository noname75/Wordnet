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
                 id=None,
                 source=None,
                 startTime=None,
                 finishTime=None,
                 minUserOnNode=None,
                 minUserOnEdge=None,
                 isDirected=None,
                 minEdgeWeight=None,
                 name=None,
                 moreInfo=None,
                 creationTime=None,
                 isActive=None):
        self.id = id
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
        self.isActive = isActive


    def addGraph(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self


    def getGraph(self):
        return db.session.query(Graph).filter_by(id=self.id).first()


    def getGraphList(self):
        return db.session.query(Graph).all()


    def changeActivationStatus(self):
        self.isActive = not self.isActive
        db.session.commit()
        return self

    def removeGraph(self, graphId):
        engine.execute(Graph.__table__.delete().where(Graph.id == graphId))


    def updateCreationTime(self, creationTime):
        self.creationTime = creationTime
        db.session.commit()