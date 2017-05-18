from blog import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://localhost\SQLExpress/wordnet?driver=ODBC+Driver+11+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Unicode(100), unique=True)
    password = db.Column(db.Unicode(60))
    firstname = db.Column(db.Unicode(100))
    lastname = db.Column(db.Unicode(100))
    email = db.Column(db.Unicode(200))
    moreinfo = db.Column(db.Unicode(1000))
    bdate = db.Column(db.Date())
    gender = db.Column(db.Enum('زن', 'مرد'))
    degree = db.Column(db.Enum('کارشناسی ارشد و دکتری', 'کارشناسی', 'فوق دیپلم', 'دیپلم', 'زیر دیپلم'))
    nativeLanguage = db.Column(db.Enum('فارسی', 'سایر زبان‌ها'))
    major = db.Column(db.Unicode(100))

    def __init__(self, username, password=None, firstname=None, lastname=None, email=None):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email


    def addUser(self):
        db.session.add(self)
        db.session.commit()

    def getUser(self):
        return db.session.query(User).filter_by(username=self.username).first()



class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(100), unique=True)
    language = db.Column(db.Enum('فارسی', 'انگلیسی', 'عربی','سایر زبان‌ها'))
    moreInfo = db.Column(db.Unicode(1000))




class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(200), unique=True)
    filePath = db.Column(db.Unicode(500))




class Phrase(db.Model):
    __tablename__ = 'phrase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Unicode(200), unique=True)
    picture_id = db.Column(db.ForeignKey(Picture.id))




class Graph(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isDirect = db.Column(db.Boolean)
    isActive = db.Column(db.Boolean, default=True)
    language = db.Column(db.Enum('فارسی', 'انگلیسی', 'عربی', 'همه‌ی زبان‌ها'))
    source = db.Column(db.Enum('پاسخ‌های کاربران سایت', 'تگ‌های اینستاگرام', 'تگ‌های اینستاگرام و پاسخ‌های کاربران سایت'))
    minWeight = db.Column(db.Float, default=0)
    minFrequency = db.Column(db.Float, default=0)
    startTime = db.Column(db.DateTime)
    finishTime = db.Column(db.DateTime)




class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    frequency = db.Column(db.Integer)




class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Unicode(50), unique=True)
    publishTime = db.Column(db.DateTime)
    storeTime = db.Column(db.DateTime)
    uid = db.Column(db.Integer)




class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.Unicode(100), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    moreInfo = db.Column(db.Unicode(1000))




class Pack(db.Model):
    __tablename__ = 'pack'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startTime = db.Column(db.DateTime())
    finishTime = db.Column(db.DateTime())
    isPictorial = db.Column(db.Boolean)
    isChosen = db.Column(db.Boolean)
    user_id = db.Column(db.ForeignKey(User.id))
    questionnaire_id = db.Column(db.ForeignKey(Questionnaire.id))

    def __init__(self, packId):
        self.id = packId

    def getPack(self):
        return db.session.query(Pack).filter_by(id=self.id).first()

    def getPackList_byUserId(userId):
        return db.session.query(Pack).filter_by(user_id=userId).all()




class PhraseInDictionary(db.Model):
    __tablename__ = '_phrase_in_dictionary'
    dictionary_id = db.Column(db.ForeignKey(Dictionary.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    weight = db.Column(db.Float)





class NodeInGraph(db.Model):
    __tablename__ = '_node_in_graph'
    weight = db.Column(db.Float)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    graph_id = db.Column(db.ForeignKey(Graph.id), primary_key=True)





class EdgeInGraph(db.Model):
    __tablename__ = '_edge_in_graph'
    weight = db.Column(db.Float)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    graph_id = db.Column(db.ForeignKey(Graph.id), primary_key=True)





class TagInPost(db.Model):
    __tablename__ = '_tag_in_post'
    number = db.Column(db.Integer)
    tag_id = db.Column(db.ForeignKey(Tag.id), primary_key=True)
    post_id = db.Column(db.ForeignKey(Post.id), primary_key=True)





class PossibleResponse(db.Model):
    __tablename__ = '_possible_response'
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)






class ResponseInPack(db.Model):
    __tablename__ = '_response_in_pack'
    duration = db.Column(db.Float)
    number = db.Column(db.Integer, primary_key=True, default=1)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    pack_id = db.Column(db.ForeignKey(Pack.id), primary_key=True)

    def getResponseList_byPackId(packId):
        return db.session.query(ResponseInPack).filter_by(pack_id=packId).all()

    def getResponseCount_byPhraseId(phraseId):
        return db.session.query(func.count(ResponseInPack.phrase2_id)).filter_by(phrase1_id=phraseId).first()


class SearchedPhrase(db.Model):
    __tablename__ = '_searched_phrase'
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)




class PhraseInQuestionnaire(db.Model):
    __tablename__ = '_phrase_in_questionnaire'
    questionnaire_id = db.Column(db.ForeignKey(Questionnaire.id), primary_key=True)
    phrase_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)

    def getPhraseList_byQuestionnaireId(questionnaireId):
        return db.session.query(PhraseInQuestionnaire).filter_by(questionnaire_id=questionnaireId).all()



def getUnseenPhraseList(packId):

    pack = Pack(packId).getPack()
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(pack.questionnaire_id)]
    packList = Pack.getPackList_byUserId(pack.user_id)
    phraseIdList_byUser = []
    for pack in packList:
        phraseIdList_byUser.extend([response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if item not in phraseIdList_byUser]
    for phraseId in unseenPhraseIdList:
        print(phraseId, ResponseInPack.getResponseCount_byPhraseId(phraseId))