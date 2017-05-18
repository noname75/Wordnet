from blog.models.db_config import *

class Phrase(db.Model):
    __tablename__ = 'phrase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Unicode(200), unique=True)
    picture_id = db.Column(db.ForeignKey(Picture.id))

    def __init__(self, phraseId):
        self.id = pharseId

    def getPhrase(self):
        return db.session.query(Phrase).filter_by(id=self.id).first()