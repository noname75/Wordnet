from blog.models.db_config import *


class PhraseController(db.Model):
    __tablename__ = '_phrase_controller'
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    credit = db.Column(db.Integer)
    type = db.Column(db.Enum('white', 'black'))