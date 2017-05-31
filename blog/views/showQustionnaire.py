from flask import render_template, Blueprint, request, session, url_for
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user
import time

showQuestionnaire_page = Blueprint('showQuestionnaire', __name__, template_folder='templates')


@app.route('/showQuestionnaire/<int:questionnaire_id>', methods=['GET'])
@user.require(http_exception=403)
def showQuestionnaire(questionnaire_id):
    return render_template('showQuestionnaire.html', questionnaire_id=questionnaire_id)


@app.route("/addPack", methods=['POST'])
@user.require(http_exception=403)
def addPack():
    questionnaireId = request.json['questionnaireId']
    isChosen = bool(int(request.json['isChosen']))
    isPictorial = bool(int(request.json['isPictorial']))

    questionnaire = Questionnaire(questionnaireId).getQuestionnaire()

    if not questionnaire.isActive or not questionnaire.isChosen == isChosen or (
                isPictorial and not questionnaire.isPictorial):
        raise AssertionError()

    pack = Pack(
        questionnaire_id=questionnaireId,
        user_id=User(session['username']).getUser().id,
        startTime=time.strftime('%Y-%m-%d %H:%M:%S'),
        isPictorial=isPictorial,
        isChosen=isChosen)

    pack.addPack()

    return url_for('questionnaire', packId=pack.id)
