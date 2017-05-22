from blog.models.db_config import *

class Phrase(db.Model):
    __tablename__ = 'phrase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Unicode(200), unique=True)
    picture_id = db.Column(db.ForeignKey(Picture.id))

    def __init__(self, phrase_id=None, content=None):
        self.id = phrase_id
        self.content = content

    def getPhrase(self):
        if self.id:
            return db.session.query(Phrase).filter_by(id=self.id).first()
        elif self.content:
            return db.session.query(Phrase).filter_by(content=self.content).first()

    def addPhrase(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def addIfNotExists(self):
        last = self.getPhrase()
        if not last:
            self.addPhrase()
            return self
        else:
            return last