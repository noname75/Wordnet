from flask import render_template, Blueprint, request, flash, redirect, url_for, jsonify
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import admin
from blog.forms.AddQuestionnaireForm import AddQuestionnaireForm
import time

questionnaireManagement_page = Blueprint('questionnaireManagement', __name__, template_folder='templates')


@app.route('/questionnaireManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def questionnaireManagement():
    questionnaireList = Questionnaire().getQuestionnaireList()
    for questionnnaire in questionnaireList:
        questionnnaire.stimulusCount = PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(
            questionnnaire.id).__len__()
    return render_template('questionnaireManagement.html', questionnaireList=questionnaireList)


@app.route('/addQuestionnaire', methods=['POST'])
@admin.require(http_exception=403)
def addQuestionnaire():
    subject = request.json['subject']
    moreInfo = request.json['moreInfo']
    stimuli = request.json['stimuli']

    questionnaire = Questionnaire(
        subject=subject,
        moreInfo=moreInfo,
        creationTime=time.strftime('%Y-%m-%d %H:%M:%S'),
        isActive=False
    ).addQuestionnaire()

    stimuliList = stimuli.split('\n')

    for s in stimuliList:
        stimulus = Phrase(content=s).addIfNotExists()
        PhraseInQuestionnaire(
            phrase_id=stimulus.id,
            questionnarire_id=questionnaire.id).addPhraseInQuestionnaire()
    return ''


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


@app.route("/changeActivationStatus", methods=['POST'])
@admin.require(http_exception=403)
def changeActivationStatus():
    questionnaireId = request.json['questionnaireId']

    questionnaire = Questionnaire(questionnaireId).getQuestionnaire()
    questionnaire.changeActivationStatus()

    return ''


@app.route("/getModalContent", methods=['POST'])
@admin.require(http_exception=403)
def getModalContent():
    questionnaireId = request.json['questionnaireId']
    questionnaire = Questionnaire(questionnaireId).getQuestionnaire()
    title = questionnaire.subject
    phraseInQuestionnaireList = PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(questionnaire.id)
    stimuliList = []
    for phraseInQuestionnaire in phraseInQuestionnaireList:
        phrase_id = phraseInQuestionnaire.phrase_id
        content = Phrase(phrase_id).getPhrase().content
        pictureForPhrase = PictureForPhrase(phrase_id=phrase_id, questionnaire_id=questionnaire.id).getPicture()
        if pictureForPhrase:
            picture = pictureForPhrase[0].decode('utf-8')[1:-1]
        else:
            picture = None
        stimuliList.append({"content": content, 'picture': picture})
    return jsonify({"title": title, 'stimuliList': stimuliList})
