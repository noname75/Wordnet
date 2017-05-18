from blog.models.db_config import *

class SearchedPhrase(db.Model):
    __tablename__ = '_searched_phrase'
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)