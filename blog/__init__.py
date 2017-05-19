from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

from blog.views.error404 import error404_page
from blog.views.unauthorized import unauthorized_page
from blog.views.index import index_page
from blog.views.login import login_page
from blog.views.logout import logout_page
from blog.views.profile import profile_page
from blog.views.questionnaire import questionnaire_page
from blog.views.register import register_page
from blog.views.questionnaireList import questionnaireList_page
from blog.views.test import test_page
from blog.views.addPack import addPack_page

app.register_blueprint(error404_page)
app.register_blueprint(unauthorized_page)
app.register_blueprint(index_page)
app.register_blueprint(login_page)
app.register_blueprint(logout_page)
app.register_blueprint(profile_page)
app.register_blueprint(register_page)
app.register_blueprint(questionnaire_page)
app.register_blueprint(questionnaireList_page)
app.register_blueprint(addPack_page)
app.register_blueprint(test_page)
# app.register_error_handler()