from blog.models.db_config import *

class EdgeInGraph(db.Model):
    __tablename__ = '_edge_in_graph'
    weight = db.Column(db.Float)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    graph_id = db.Column(db.ForeignKey(Graph.id), primary_key=True)

    def getEdges_byGraphId(self, graph_id):
        return db.session.query(EdgeInGraph).filter_by(graph_id=graph_id).all()

    def getEdges_byGraphId(self, graph_id):
        return db.session.query(EdgeInGraph).filter_by(graph_id=graph_id).all()