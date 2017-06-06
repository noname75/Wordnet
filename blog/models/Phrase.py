from blog.models.db_config import *
import time
class Phrase(db.Model):
    __tablename__ = 'phrase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Unicode(200), unique=True)

    def __init__(self, phrase_id=None, content=None, creationTime=None):
        self.id = phrase_id
        self.content = content
        self.creationTime = creationTime

    def getPhrase(self):
        return db.session.query(Phrase).filter_by(id=self.id).first()

    def getPhrase_byContent(self):
            return db.session.query(Phrase).filter_by(content=self.content).first()

    def addPhrase(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def addIfNotExists(self):
        last = self.getPhrase_byContent()
        if not last:
            self.addPhrase()
            return self
        else:
            return last


    def getAllPhrases(self):
        return db.session.query(Phrase).all()