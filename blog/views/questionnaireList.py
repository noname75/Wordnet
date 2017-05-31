from flask import render_template, Blueprint, redirect, request, session, url_for, jsonify
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user, admin
import time

questionnaireList_page = Blueprint('questionnaireList', __name__, template_folder='templates')


@app.route('/questionnaireList/<int:isChosen>', methods=['GET'])
@user.require(http_exception=403)
def questionnaireList(isChosen):
        user = User(username=session['username']).getUser()
        questionnaireList = Questionnaire.getQuestionnaireList(isChosen)
        for questionnnaire in questionnaireList:
            questionnnaire.stimulusCount = PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(
                questionnnaire.id).__len__()
            questionnnaire.isCompletedByUser = isCompletedByUser(questionnnaire.id, user.id)
        return render_template('questionnaireList.html',
                               questionnaireList=questionnaireList)


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
    hasPicStimuliList = []
    hasNotPicStimuliList = []
    for phraseInQuestionnaire in phraseInQuestionnaireList:
        phrase_id = phraseInQuestionnaire.phrase_id
        content = Phrase(phrase_id).getPhrase().content
        if PictureForPhrase(questionnaire_id=questionnaireId, phrase_id=phrase_id).getPicture():
            hasPicStimuliList.append(content)
        else:
            hasNotPicStimuliList.append(content)

    hasPicStr = ', '.join(hasPicStimuliList)
    hasNotPicStr = ', '.join(hasNotPicStimuliList)
    return jsonify({"title": title, 'hasPicStr': hasPicStr, 'hasNotPicStr': hasNotPicStr})


def isCompletedByUser(questionnaire_id, user_id):
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in
                                  PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(questionnaire_id)]
    packList = Pack.getPackList_byQuestionnaireIdAndUserId(questionnaire_id, user_id)
    phrase_phraseIdList_byUser = []
    picture_phraseIdList_byUser = []
    for pack in packList:
        if pack.isPictorial:
            picture_phraseIdList_byUser.extend(
                [response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
        else:
            phrase_phraseIdList_byUser.extend(
                [response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])

    unseenPicture_phraseIdList = [item for item in phraseList_byQuestionnaire if
                                  (item not in picture_phraseIdList_byUser) and PictureForPhrase(phrase_id=item,
                                                                                                 questionnaire_id=questionnaire_id).getPicture()]
    unseenPhrase_phraseIdList = [item for item in phraseList_byQuestionnaire if item not in phrase_phraseIdList_byUser]
    if unseenPhrase_phraseIdList.__len__() == 0 and unseenPicture_phraseIdList.__len__() == 0:
        return True
    else:
        return False