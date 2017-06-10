from blog.models.db_config import *

class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.Unicode(100))
    picture = db.Column(db.VARBINARY)
    moreInfo = db.Column(db.Unicode(1000))
    isActive = db.Column(db.Boolean, default=False)
    creationTime = db.Column(db.DateTime())


    def __init__(self,
                 questionnaire_id=None,
                 moreInfo=None,
                 subject=None,
                 isActive=None,
                 picture=None,
                 creationTime=None):

        self.id = questionnaire_id
        self.subject = subject
        self.isActive = isActive
        self.moreInfo = moreInfo
        self.picture = picture
        self.creationTime = creationTime

    def addQuestionnaire(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self


    def changeActivationStatus(self):
        self.isActive = not self.isActive
        db.session.commit()
        return self


    def getQuestionnaireList(self):
        return db.session.query(Questionnaire).all()


    def getQuestionnaire(self):
        if self.id:
            return db.session.query(Questionnaire).filter_by(id=self.id).first()
        elif self.subject:
            return db.session.query(Questionnaire).filter_by(subject=self.subject).first()
