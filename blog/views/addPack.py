import time

from flask import Blueprint, redirect, url_for, session

from blog import app


addPack_page = Blueprint('addPack', __name__)


@app.route('/addPack/<questionnaireId>/<questionnaireType>')
def addPack(questionnaireId, questionnaireType):
    isPictorial = 'pic' in questionnaireType
    isChosen = 'cho' in questionnaireType

    pack = Pack(
        questionnaire_id=questionnaireId,
        user_id=User(session['username']).getUser().id,
        startTime=time.strftime('%Y-%m-%d %H:%M:%S'),
        isPictorial=isPictorial,
        isChosen=isChosen)
    pack.addPack()

    return redirect(url_for('questionnaire', packId=pack.id))
