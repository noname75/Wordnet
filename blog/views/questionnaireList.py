from flask import render_template, Blueprint, redirect, request
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user

questionnaireList_page = Blueprint('questionnaireList', __name__, template_folder='templates')

@app.route('/questionnaireList/<questionnaireType>')
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
