from blog.models.db_config import *
from flask import request, render_template, Blueprint, session, redirect, flash, jsonify, url_for
from blog import app
from blog.views.permission_config import user
import random
import time

pack_page = Blueprint('pack', __name__, template_folder='templates')


@app.route('/pack/<int:packId>', methods=['GET'])
@user.require(http_exception=403)
def pack(packId):
    pack = Pack(pack_id=packId).getPack()

    if pack.user_id != User(username=session['username']).getUser().id:
        return redirect('authorisation_failed')

    return render_template('pack.html', packId=packId, isPictorial=pack.isPictorial)


@app.route('/addResponse', methods=['POST'])
@user.require(http_exception=403)
def addResponse():
    stimulus = request.json['stimulusId']
    response = request.json['response']
    packId = request.json['packId']
    duration = request.json['duration']

    response = Phrase(content=response).addIfNotExists()

    ResponseInPack(pack_id=packId,
                   phrase1_id=stimulus,
                   phrase2_id=response.id,
                   duration=duration).addResponseInPack()
    return ''


@app.route('/getStimulus', methods=['POST'])
@user.require(http_exception=403)
def getStimulus():
    packId = request.json['packId']
    pack = Pack(pack_id=packId).getPack()

    unansweredPhraseId = ResponseInPack(pack_id=pack.id).unansweredPhraseId()
    if not unansweredPhraseId:
        unseenPhraseIdList = getUnseenPhraseIdList(pack.id)
        if unseenPhraseIdList.__len__() == 0:
            pack.setFinishTime(time.strftime('%Y-%m-%d %H:%M:%S'))
            flash(message='شما به تمامی سوالات پرسش‌نامه پاسخ دادید.', category='success')
            return url_for('index')
        stimulusId = random.choice(unseenPhraseIdList)
        ResponseInPack(pack_id=pack.id, phrase1_id=stimulusId).addResponseInPack()
    else:
        stimulusId = unansweredPhraseId[0]

    if pack.isPictorial:
        pictureForPhrase = PictureForPhrase(phrase_id=stimulusId, questionnaire_id=pack.questionnaire_id).getPicture()[
            0]
        stimulus = pictureForPhrase.decode('utf-8')[1:-1]
    else:
        stimulus = Phrase(phrase_id=stimulusId).getPhrase().content
    return jsonify({'stimulusId': stimulusId, 'stimulus': stimulus, 'isPictorial': pack.isPictorial})


@app.route('/endQuestionnaire', methods=['POST'])
@user.require(http_exception=403)
def endQuestionnaire():
    packId = request.json['packId']
    pack = Pack(pack_id=packId).getPack()

    pack.setFinishTime(time.strftime('%Y-%m-%d %H:%M:%S'))
    flash(message='پرسشنامه با موفقیت تکمیل شد. ممنون از مشارکت شما.', category='success')
    return url_for('index')


def getUnseenPhraseIdList(packId):
    pack = Pack(pack_id=packId).getPack()
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in
                                  PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(pack.questionnaire_id)]
    packList = Pack.getPackList_byQuestionnaireIdAndUserId(pack.questionnaire_id, pack.user_id)
    phrase_phraseIdList_byUser = []
    picture_phraseIdList_byUser = []
    for pack in packList:
        if pack.isPictorial:
            picture_phraseIdList_byUser.extend(
                [response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
        else:
            phrase_phraseIdList_byUser.extend(
                [response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    if pack.isPictorial:
        unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if
                              (item not in picture_phraseIdList_byUser) and PictureForPhrase(phrase_id=item,
                                                                                     questionnaire_id=pack.questionnaire_id).getPicture()]
    else:
        unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if item not in phrase_phraseIdList_byUser]
    return unseenPhraseIdList