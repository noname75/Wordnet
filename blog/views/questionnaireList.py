from flask import render_template, Blueprint, redirect, request, session, url_for
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user
import time

questionnaireList_page = Blueprint('questionnaireList', __name__, template_folder='templates')


@app.route('/questionnaireList/<questionnaireType>', methods=['GET'])
@user.require(http_exception=403)
def questionnaireList(questionnaireType):
    try:
        questionnaireList = Questionnaire.getQuestionnaireList(questionnaireType)
        for questionnnaire in questionnaireList:
            questionnnaire.setStimulusCount(
                PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(questionnnaire.id).__len__())
        return render_template('questionnaireList.html',
                               questionnaireList=questionnaireList,
                               questionnaireType=questionnaireType)

    except Exception:
        return redirect('page_not_found')


@app.route("/addPack", methods=['POST'])
@user.require(http_exception=403)
def addPack():
    questionnaireId = request.json['questionnaireId']
    questionnaireType = request.json['questionnaireType']

    questionnaire = Questionnaire(questionnaireId).getQuestionnaire()

    if not questionnaire.isActive:
        raise AssertionError()

    if questionnaireType == '00':
        isPictorial = 0
        isChosen = 0
    elif questionnaireType == '01':
        isPictorial = 0
        isChosen = 1
        if not questionnaire.isChosen:
            raise AssertionError()
    elif questionnaireType == '10':
        isPictorial = 1
        isChosen = 0
        if not questionnaire.isPictorial:
            raise AssertionError()
    elif questionnaireType == '11':
        isPictorial = 1
        isChosen = 1
        if not questionnaire.isChosen or not questionnaire.isPictorial:
            raise AssertionError()

    pack = Pack(
        questionnaire_id=questionnaireId,
        user_id=User(session['username']).getUser().id,
        startTime=time.strftime('%Y-%m-%d %H:%M:%S'),
        isPictorial=isPictorial,
        isChosen=isChosen)

    pack.addPack()

    return url_for('questionnaire', packId=pack.id)

