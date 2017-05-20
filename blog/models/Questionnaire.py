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


    def __init__(self, questionnaire_id=None, moreInfo=None, subject=None, isActive=False, isPictorial=False,
                 isChosen=False):
        self.id = questionnaire_id
        self.subject = subject
        self.isActive = isActive
        self.isPictorial = isPictorial
        self.isChosen = isChosen
        self.moreInfo = moreInfo

    def getQuestionnaire(self):
        if self.id:
            return db.session.query(Questionnaire).filter_by(id=self.id).first()
        elif self.subject:
            return db.session.query(Questionnaire).filter_by(subject=self.subject).first()

    def setStimulusCount(self, stimulusCount):
        self.stimulusCount = stimulusCount

    def setUserResponseCount(self, userResponseCount):
        self.userResponseCount = userResponseCount


    def addQuestionnaire(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

        return self