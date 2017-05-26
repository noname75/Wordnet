from flask import render_template, Blueprint, request, flash, redirect, url_for
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import admin
from blog.forms.AddQuestionnaireForm import AddQuestionnaireForm

editQuestionnaire_page = Blueprint('editQuestionnaire', __name__, template_folder='templates')


@app.route('/editQuestionnaire/<int:questionnaire_id>', methods=['GET'])
@admin.require(http_exception=403)
def editQuestionnaire(questionnaire_id):
    phraseInQuestionnaireList = PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(questionnaire_id)
    for phraseInQuestionnaire in phraseInQuestionnaireList:
        phraseInQuestionnaire.content = Phrase(phrase_id=phraseInQuestionnaire.phrase_id).getPhrase().content
        phraseInQuestionnaire.picture = PictureForPhrase(phrase_id=phraseInQuestionnaire.phrase_id,
                                                         questionnaire_id=questionnaire_id).getPicture()
        phraseInQuestionnaire.responseList = PossibleResponse(phrase1_id=phraseInQuestionnaire.phrase_id,
                                                              questionnaire_id=questionnaire_id).getPossibleResponseList()

    return render_template('editQuestionnaire.html', phraseList=phraseInQuestionnaireList)
