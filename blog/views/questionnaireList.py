from flask import render_template, Blueprint
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user

questionnaireList_page = Blueprint('questionnaireList', __name__, template_folder='templates')

@app.route('/questionnaireList/<questionnaireType>')
@user.require(http_exception=403)
def questionnaireList(questionnaireType):
    questionnaireList = Questionnaire.getQuestionnaireList(questionnaireType)
    return render_template('questionnaireList.html',
                           questionnaireList=questionnaireList,
                           questionnaireType=questionnaireType)

