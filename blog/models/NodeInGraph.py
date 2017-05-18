from blog.models.db_config import *

class NodeInGraph(db.Model):
    __tablename__ = '_node_in_graph'
    weight = db.Column(db.Float)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    graph_id = db.Column(db.ForeignKey(Graph.id), primary_key=True)