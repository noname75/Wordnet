from blog.models.db_config import *

class TagInPost(db.Model):
    __tablename__ = '_tag_in_post'
    number = db.Column(db.Integer)
    tag_id = db.Column(db.ForeignKey(Tag.id), primary_key=True)
    post_id = db.Column(db.ForeignKey(Post.id), primary_key=True)