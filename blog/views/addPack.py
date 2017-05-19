import time
import random
from blog.models.db_config import *
from flask import Blueprint, redirect, url_for, session
from blog import app
from blog import config
from blog.views.permission_config import user

addPack_page = Blueprint('addPack', __name__, template_folder='templates')

@app.route("/addPack/<questionnaireId>/<questionnaireType>")
@user.require(http_exception=403)
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

    phraseId_freq = getUnseenPhraseListWithFreq(pack.id)
    samplePhraseIdList = random.sample(list(phraseId_freq.keys()), config.STIMULUS_COUNT)
    # samplePhraseIdList = np.random.choice(phraseId_freq.keys(), 10, p=normalize(phraseId_freq.values()))

    for phraseId in samplePhraseIdList:
        responseInPack = ResponseInPack(pack_id=pack.id, phrase1_id=phraseId)
        responseInPack.addResponseInPack()

    return redirect(url_for('questionnaire', packId=pack.id))


def getUnseenPhraseListWithFreq(packId):
    phraseId_freq = {}
    pack = Pack(pack_id=packId).getPack()
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in
                                  PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(pack.questionnaire_id)]
    packList = Pack.getPackList_byUserId(pack.user_id)
    phraseIdList_byUser = []
    for pack in packList:
        phraseIdList_byUser.extend(
            [response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if item not in phraseIdList_byUser]
    for phraseId in unseenPhraseIdList:
        phraseId_freq[phraseId] = ResponseInPack.getResponseCount_byPhraseId(phraseId)
    return phraseId_freq


def normalize(freq_list):
    inverse_freq_list = [1 / (member + 1) for member in freq_list]
    normalized_inverse_freq_list = [member / sum(inverse_freq_list) for member in inverse_freq_list]
    return normalized_inverse_freq_list