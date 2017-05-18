from blog.models.db_config import *

class PhraseInDictionary(db.Model):
    __tablename__ = '_phrase_in_dictionary'
    dictionary_id = db.Column(db.ForeignKey(Dictionary.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    weight = db.Column(db.Float)