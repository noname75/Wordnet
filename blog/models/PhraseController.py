from blog.models.db_config import *


class PhraseController(db.Model):
    __tablename__ = '_phrase_controller'
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    credit = db.Column(db.Integer, default=0)
    type = db.Column(db.Enum('white', 'black'))

    def __init__(self, phrase_id, type=None):
        self.phrase_id = phrase_id
        self.type = type

    def getPhraseController(self):
        return db.session.query(PhraseController).filter_by(phrase_id=self.phrase_id).first()


    def addPhraseController(self):
        db.session.add(self)
        db.session.commit()

    def updateType(self, type):
        self.type = type
        db.session.commit()

    def creditPlusOne(self):
        self.credit = self.credit + 1
        db.session.commit()