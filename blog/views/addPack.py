import time
from hashids import Hashids
from blog.models.db_config import *
from flask import Blueprint, redirect, url_for, session, render_template
from blog import app
from blog.views.permission_config import user


addPack_page = Blueprint('addPack', __name__, template_folder='templates')

@app.route("/addPack/<questionnaireId>/<questionnaireType>")
@user.require(http_exception=403)
def addPack(questionnaireId, questionnaireType):
    questionnaire = Questionnaire(questionnaireId).getQuestionnaire()

    if questionnaire.isActive:
        if questionnaireType == '00':
            isPictorial = 0
            isChosen = 0
        elif questionnaireType == '01':
            isPictorial = 0
            isChosen = 1
            if not questionnaire.isChosen:
                redirect('page_not_found')
        elif questionnaireType == '10':
            isPictorial = 1
            isChosen = 0
            if not questionnaire.isPictorial:
                redirect('page_not_found')
        elif questionnaireType == '11':
            isPictorial = 1
            isChosen = 1
            if not questionnaire.isChosen or not questionnaire.isPictorial:
                redirect('page_not_found')
    else:
        redirect('page_not_found')

    if not questionnaire:
        return redirect('page_not_found')

    pack = Pack(
        questionnaire_id=questionnaireId,
        user_id=User(session['username']).getUser().id,
        startTime=time.strftime('%Y-%m-%d %H:%M:%S'),
        isPictorial=isPictorial,
        isChosen=isChosen)
    pack.addPack()

    return redirect(url_for('questionnaire', packId=pack.id))