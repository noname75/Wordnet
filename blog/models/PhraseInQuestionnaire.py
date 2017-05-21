from blog.models.db_config import *

class PhraseInQuestionnaire(db.Model):
    __tablename__ = '_phrase_in_questionnaire'
    questionnaire_id = db.Column(db.ForeignKey(Questionnaire.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)

    def getPhraseList_byQuestionnaireId(questionnaire_id):
        return db.session.query(PhraseInQuestionnaire).filter_by(questionnaire_id=questionnaire_id).all()

    def __init__(self, questionnarire_id, phrase_id):
        self.questionnaire_id = questionnarire_id
        self.phrase_id = phrase_id

    def addPhraseInQuestionnaire(self):
        if not db.session.query(PhraseInQuestionnaire).filter_by(questionnaire_id=self.questionnaire_id,
                                                             phrase_id=self.phrase_id).first():
            db.session.add(self)
            db.session.commit()