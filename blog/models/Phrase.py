from blog.models.db_config import *
import time
class Phrase(db.Model):
    __tablename__ = 'phrase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Unicode(200), unique=True)

    def __init__(self, phrase_id=None, content=None):
        self.id = phrase_id
        self.content = content


    def getPhrase(self):
        rslt = engine.execute("select id, content from phrase where id=?", self.id).fetchone()
        if rslt:
            return Phrase(rslt[0], rslt[1])
        else:
            return None


    def getPhrase_byContent(self):
        rslt = engine.execute("select id, content from phrase where content=?", self.content).fetchone()
        if rslt:
            return Phrase(rslt[0], rslt[1])
        else:
            return None


    def addIfNotExists(self):
        last = self.getPhrase_byContent()
        if not last:
            engine.execute("INSERT INTO phrase (content) VALUES (?)", self.content)
            return self.getPhrase_byContent()
        else:
            return last
