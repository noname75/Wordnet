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
        if questionnaireType == 'tex-des':
            return db.session.query(Questionnaire).filter_by(isActive=True).all()
        elif questionnaireType == 'pic-des':
            return db.session.query(Questionnaire).filter_by(isActive=True, isPictorial=True).all()
        elif questionnaireType == 'tex-cho':
            return db.session.query(Questionnaire).filter_by(isActive=True, isChosen=True).all()
        elif questionnaireType == 'pic-cho':
            return db.session.query(Questionnaire).filter_by(isActive=True, isPictorial=True, isChosen=True).all()