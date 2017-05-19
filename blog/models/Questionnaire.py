from blog.models.db_config import *

class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.Unicode(100), unique=True)
    isActive = db.Column(db.Boolean, default=True)
    isPictorial = db.Column(db.Boolean, default=False)
    isChosen = db.Column(db.Boolean, default=False)
    moreInfo = db.Column(db.Unicode(1000))

    def getQuestionnaireList(questionnaireType):
        if questionnaireType == '00':
            return db.session.query(Questionnaire).filter_by(isActive=True).all()
        elif questionnaireType == '01':
            return db.session.query(Questionnaire).filter_by(isActive=True, isPictorial=True).all()
        elif questionnaireType == '10':
            return db.session.query(Questionnaire).filter_by(isActive=True, isChosen=True).all()
        elif questionnaireType == '11':
            return db.session.query(Questionnaire).filter_by(isActive=True, isPictorial=True, isChosen=True).all()
        else:
            return None


    def __init__(self, questionnaire_id):
        self.id = questionnaire_id

    def getQuestionnaire(self):
        return db.session.query(Questionnaire).filter_by(id=self.id).first()