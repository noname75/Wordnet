from blog.models.db_config import *


class PhraseController(db.Model):
    __tablename__ = '_phrase_controller'
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    credit = db.Column(db.Integer, default=0)
    type = db.Column(db.Enum('white', 'black'))

    def __init__(self, phrase_id, type=None, credit=0):
        self.phrase_id = phrase_id
        self.type = type
        self.credit = credit

    def getPhraseController(self):
        rslt = engine.execute("select phrase_id, type, credit from _phrase_controller where phrase_id=?",
                              self.phrase_id).fetchone()
        if rslt:
            return PhraseController(rslt[0], rslt[1], rslt[2])
        else:
            return None


    def addPhraseController(self):
        engine.execute("INSERT INTO _phrase_controller (phrase_id,type) VALUES (?,?)", self.phrase_id, self.type)

    def updateType(self, type):
        self.type = type
        db.session.commit()

    def creditPlusOne(self):
        self.credit = self.credit + 1
        db.session.commit()