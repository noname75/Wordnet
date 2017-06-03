from blog.models.db_config import *

class Pack(db.Model):
    __tablename__ = 'pack'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startTime = db.Column(db.DateTime(), nullable=False)
    finishTime = db.Column(db.DateTime())
    isPictorial = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    questionnaire_id = db.Column(db.ForeignKey(Questionnaire.id), nullable=False)
    isChecked = db.Column(db.Boolean)

    def __init__(
            self,
            pack_id=None,
            questionnaire_id=None,
            user_id=None,
            startTime=None,
            isPictorial=None,
            isChecked=None):

        self.id = pack_id
        self.questionnaire_id = questionnaire_id
        self.user_id = user_id
        self.startTime = startTime
        self.isPictorial = isPictorial
        self.isChecked = isChecked

    def getPack(self):
        return db.session.query(Pack).filter_by(id=self.id).first()

    def getPackList_byUserId(userId):
        return db.session.query(Pack).filter_by(user_id=userId).all()

    def getPackList_byQuestionnaireId(questionnaireId):
        return db.session.query(Pack).filter_by(questionnaire_id=questionnaireId).all()

    def getPackList_byQuestionnaireIdAndUserId(questionnaireId, userId):
        return db.session.query(Pack).filter_by(questionnaire_id=questionnaireId, user_id=userId)

    def addPack(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def setFinishTime(self, finishTime):
        self.finishTime = finishTime
        db.session.commit()


    def getPackList_byIsChecked(self, isChecked):
        return db.session.query(Pack).filter_by(isChecked=isChecked).all()


    def setIsChecked(self, isChecked):
        self.isChecked = isChecked
        db.session.commit()