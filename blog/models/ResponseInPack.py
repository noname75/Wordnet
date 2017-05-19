from sqlalchemy import func
from blog.models.db_config import *


class ResponseInPack(db.Model):
    __tablename__ = '_response_in_pack'
    duration = db.Column(db.Float)
    number = db.Column(db.Integer, primary_key=True, default=1)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id))
    pack_id = db.Column(db.ForeignKey(Pack.id), primary_key=True)

    def getResponseList_byPackId(pack_id):
        return db.session.query(ResponseInPack).filter_by(pack_id=pack_id).all()

    def getResponseCount_byPhraseId(phrase_id):
        return db.session.query(func.count(ResponseInPack.phrase2_id)).filter_by(phrase1_id=phrase_id).scalar()

    def __init__(self, pack_id, phrase1_id, phrase2_id=None, duration=None):
        self.pack_id = pack_id
        self.phrase1_id = phrase1_id
        self.phrase2_id = phrase2_id
        self.duration = duration

    def addResponseInPack(self):
        maxNumber = db.session.query(func.max(ResponseInPack.number)).filter_by(phrase1_id=self.phrase1_id,
                                                                                pack_id=self.pack_id).scalar()
        if maxNumber:
            self.number = maxNumber + 1
        db.session.add(self)
        db.session.commit()

        return self