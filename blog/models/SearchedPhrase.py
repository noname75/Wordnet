from blog.models.db_config import *

class SearchedPhrase(db.Model):
    __tablename__ = '_searched_phrase'
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    time = db.Column(db.DateTime)


    def __init__(self, user_id, phrase_id, time):
        self.user_id = user_id
        self.phrase_id = phrase_id
        self.time = time

    def getSearchedPhrase(self):
        return db.session.query(SearchedPhrase).filter_by(user_id=self.user_id, phrase_id=self.phrase_id).first()


    def addSearchedPhrase(self):
        db.session.add(self)
        db.session.commit()


    def addIfNotExists(self):
        if not self.getSearchedPhrase():
            self.addSearchedPhrase()