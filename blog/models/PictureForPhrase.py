from blog.models.db_config import *


class PictureForPhrase(db.Model):
    __tablename__ = '_picture_for_phrase'
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    questionnaire_id = db.Column(db.ForeignKey(Questionnaire.id), primary_key=True)
    picture = db.Column(db.VARBINARY, nullable=False)


    def __init__(self, phrase_id, questionnaire_id, picture=None):
        self.questionnaire_id = questionnaire_id
        self.phrase_id = phrase_id
        self.picture = picture

    def getPicture(self):
        return db.session.query(PictureForPhrase.picture).filter_by(phrase_id=self.phrase_id,
                                                                    questionnaire_id=self.questionnaire_id).first()

    def addPictureForPhrase(self):
        db.session.add(self)
        db.session.commit()