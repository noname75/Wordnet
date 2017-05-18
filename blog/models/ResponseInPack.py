from blog.models.db_config import *

class ResponseInPack(db.Model):
    __tablename__ = '_response_in_pack'
    duration = db.Column(db.Float)
    number = db.Column(db.Integer, primary_key=True, default=1)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    pack_id = db.Column(db.ForeignKey(Pack.id), primary_key=True)

    def getResponseList_byPackId(packId):
        return db.session.query(ResponseInPack).filter_by(pack_id=packId).all()

    def getResponseCount_byPhraseId(phraseId):
        return db.session.query(func.count(ResponseInPack.phrase2_id)).filter_by(phrase1_id=phraseId).first()