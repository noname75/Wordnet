from blog.models.db_config import *

class NodeInGraph(db.Model):
    __tablename__ = '_node_in_graph'
    weight = db.Column(db.Float)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    graph_id = db.Column(db.ForeignKey(Graph.id), primary_key=True)

    def __init__(self, weight=None, phrase_id=None, graph_id=None):
        self.weight = weight
        self.phrase_id = phrase_id
        self.graph_id = graph_id

    def getNodes_byGraphId(self, graph_id):
        return db.session.query(NodeInGraph).filter_by(graph_id=graph_id).all()

    def getNodes_byNodeIdList(self, graph_id, nodeInGraphIdList):
        return db.session.query(NodeInGraph).filter_by(graph_id=graph_id).filter(
            NodeInGraph.phrase_id.in_(nodeInGraphIdList))



    def addNodeInGraph(self):
        engine.execute(NodeInGraph.__table__.insert(), self.__dict__)

    def removeNodes_byGraphId(self, graphId):
        engine.execute(NodeInGraph.__table__.delete().where(NodeInGraph.graph_id == graphId))
