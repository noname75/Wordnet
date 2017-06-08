from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
import json

from blog import app

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://localhost\SQLExpress/wordnet?driver=ODBC+Driver+11+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
engine = create_engine("mssql+pyodbc://localhost\SQLExpress/wordnet?driver=ODBC+Driver+11+for+SQL+Server", echo=False)

from blog.models.User import User
from blog.models.Phrase import Phrase
from blog.models.Graph import Graph
from blog.models.Questionnaire import Questionnaire
from blog.models.Pack import Pack
from blog.models.Post import Post

from blog.models.SearchedPhrase import SearchedPhrase
from blog.models.ResponseInPack import ResponseInPack
from blog.models.EdgeInGraph import EdgeInGraph
from blog.models.NodeInGraph import NodeInGraph
from blog.models.PhraseController import PhraseController
from blog.models.PhraseInQuestionnaire import PhraseInQuestionnaire
from blog.models.PictureForPhrase import PictureForPhrase

