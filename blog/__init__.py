from flask import Flask

app = Flask(__name__)

from blog.views.errorhandler import error404_page
from blog.views.index import index_page
from blog.views.login import login_page
from blog.views.logout import logout_page
from blog.views.profile import profile_page
from blog.views.questionnaire import questionnaire_page
from blog.views.register import register_page
from blog.views.test import test_page

app.register_blueprint(error404_page)
app.register_blueprint(index_page)
app.register_blueprint(login_page)
app.register_blueprint(logout_page)
app.register_blueprint(profile_page)
app.register_blueprint(questionnaire_page)
app.register_blueprint(register_page)
app.register_blueprint(test_page)
