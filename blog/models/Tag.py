from blog.models.db_config import *

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    frequency = db.Column(db.Integer)