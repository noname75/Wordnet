from blog.models.db_config import *

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Unicode(100), unique=True)
    password = db.Column(db.Unicode(60))
    role = db.Column(db.Enum('admin', 'user'))
    firstname = db.Column(db.Unicode(100))
    lastname = db.Column(db.Unicode(100))
    email = db.Column(db.Unicode(200))
    moreinfo = db.Column(db.Unicode(1000))
    bdate = db.Column(db.Date())
    gender = db.Column(db.Enum('زن', 'مرد'))
    degree = db.Column(db.Enum('کارشناسی ارشد و دکتری', 'کارشناسی', 'فوق دیپلم', 'دیپلم', 'زیر دیپلم'))
    nativeLanguage = db.Column(db.Enum('فارسی', 'سایر زبان‌ها'))
    major = db.Column(db.Unicode(100))
    registerationTime = db.Column(db.DateTime())

    def __init__(
            self,
            user_id=None,
            username=None,
            password=None,
            firstname=None,
            lastname=None,
            email=None,
            registerationTime=None,
            role='user'):

        self.id = user_id
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = role
        self.registerationTime = registerationTime

    def addUser(self):
        db.session.add(self)
        db.session.commit()

    def getUser(self):
        if self.username:
            return db.session.query(User).filter_by(username=self.username).first()
        elif self.id:
            return db.session.query(User).filter_by(username=self.id).first()
