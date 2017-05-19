from blog.models.db_config import *

class PhraseInQuestionnaire(db.Model):
    __tablename__ = '_phrase_in_questionnaire'
    questionnaire_id = db.Column(db.ForeignKey(Questionnaire.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)

    def getPhraseList_byQuestionnaireId(questionnaire_id):
        return db.session.query(PhraseInQuestionnaire).filter_by(questionnaire_id=questionnaire_id).all()