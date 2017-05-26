from blog.models.db_config import *

class PossibleResponse(db.Model):
    __tablename__ = '_possible_response'
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    questionnaire_id = db.Column(db.ForeignKey(Questionnaire.id), primary_key=True)


    def __init__(self, phrase1_id, questionnaire_id):
        self.phrase1_id = phrase1_id
        self.questionnaire_id = questionnaire_id


    def getPossibleResponseList(self):
        return db.session.query(PossibleResponse).filter_by(phrase1_id=self.phrase1_id,
                                                            questionnaire_id=self.questionnaire_id).all()