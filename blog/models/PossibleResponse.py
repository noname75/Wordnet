from blog.models.db_config import *

class PossibleResponse(db.Model):
    __tablename__ = '_possible_response'
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)