from flask import render_template, Blueprint, request, jsonify, flash
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import admin
import json

editQuestionnaire_page = Blueprint('editQuestionnaire', __name__, template_folder='templates')


@app.route('/editQuestionnaire/<int:questionnaire_id>', methods=['GET'])
@admin.require(http_exception=403)
def editQuestionnaire(questionnaire_id):
    return render_template('editQuestionnaire.html', questionnaire_id=questionnaire_id)


@app.route('/getPhrases', methods=['POST'])
@admin.require(http_exception=403)
def getPhrases():
    questionnaire_id = request.json['questionnaire_id']
    phraseList = []
    phraseInQuestionnaireList = PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(questionnaire_id)
    for phraseInQuestionnaire in phraseInQuestionnaireList:
        phraseInQuestionnaire.content = Phrase(phrase_id=phraseInQuestionnaire.phrase_id).getPhrase().content
        if not PictureForPhrase(phrase_id=phraseInQuestionnaire.phrase_id,
                                questionnaire_id=questionnaire_id).getPicture():
            phraseList.append({
                'content': Phrase(phraseInQuestionnaire.phrase_id).getPhrase().content,
                'id': phraseInQuestionnaire.phrase_id
            })
    phraseList = sorted(phraseList, key=lambda k: k['content'].__len__())
    return jsonify({'phraseList': phraseList})


@app.route('/setPicture', methods=['POST'])
@admin.require(http_exception=403)
def setPicture():
    phrase_id = request.json['phrase_id']
    picture = bytes(json.dumps(request.json['picture']), 'utf8')
    questionnaire_id = request.json['questionnaire_id']

    PictureForPhrase(phrase_id=phrase_id, picture=picture, questionnaire_id=questionnaire_id).addPictureForPhrase()
    return ''
