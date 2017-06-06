from blog.models.db_config import *
from sqlalchemy import or_, and_

class EdgeInGraph(db.Model):
    __tablename__ = '_edge_in_graph'
    weight = db.Column(db.Float)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    graph_id = db.Column(db.ForeignKey(Graph.id), primary_key=True)


    def __init__(self, weight=None, phrase1_id=None, phrase2_id=None, graph_id=None):
        self.weight = weight
        self.phrase1_id = phrase1_id
        self.phrase2_id = phrase2_id
        self.graph_id = graph_id

    def getEdges_byGraphId(self, graph_id):
        return db.session.query(EdgeInGraph).filter_by(graph_id=graph_id).all()

    def getEdges_byGraphId(self, graph_id):
        return db.session.query(EdgeInGraph).filter_by(graph_id=graph_id).all()

    def getEgoNet_byGraphId(self, graph_id, nodeIdList):
        return db.session.query(EdgeInGraph).filter(
            and_(
                or_(
                    EdgeInGraph.phrase1_id.in_(nodeIdList),
                    EdgeInGraph.phrase2_id.in_(nodeIdList)
                ),
                EdgeInGraph.graph_id == graph_id
            )
        ).all()


    def addEdgeInGraph(self):
        db.session.add(self)
        db.session.commit()