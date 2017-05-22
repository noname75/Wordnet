from blog.models.db_config import *

class EdgeInGraph(db.Model):
    __tablename__ = '_edge_in_graph'
    weight = db.Column(db.Float)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    graph_id = db.Column(db.ForeignKey(Graph.id), primary_key=True)

    def getEdges_byGraphId(self, graph_id):
        source = db.session.query(EdgeInGraph.phrase1_id).filter_by(graph_id=graph_id).all()
        dest = db.session.query(EdgeInGraph.phrase2_id).filter_by(graph_id=graph_id).all()
        weight = db.session.query(EdgeInGraph.weight).filter_by(graph_id=graph_id).all()

        return source, dest, weight