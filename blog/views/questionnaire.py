from blog.models.db_config import *
from flask import request, render_template, Blueprint, session, redirect, flash
from blog import app
from blog.forms.QuestionnaireForm import QuestionnaireForm
from blog.views.permission_config import user
import random
from blog import config
import time


questionnaire_page = Blueprint('questionnaire', __name__, template_folder='templates')

@app.route('/questionnaire/<packId>', methods=['GET', 'POST'])
@user.require(http_exception=403)
def questionnaire(packId):

    form = QuestionnaireForm(request.form)
    error = None

    pack = Pack(pack_id=packId).getPack()
    if not pack:
        redirect('page_not_found')
    if User(user_id=pack.user_id).username != session['username']:
        redirect('authorisation_failed')

    packResponseCount = ResponseInPack.getResponseList_byPackId(pack.id).__len__()

    if packResponseCount >= config.STIMULUS_COUNT:
        pack.setFinishTime(time.strftime('%Y-%m-%d %H:%M:%S'))
        flash(message='پرسشنامه با موفقیت تکمیل شد. ممنون از مشارکت شما.', category='success')
        return redirect('/')

    unseenPhraseIdList = getUnseenPhraseIdList(pack.id)
    stimulusId = random.choice(unseenPhraseIdList)
    # stimulusList = np.random.choice(phraseId_freq.keys(), 10, p=normalize(phraseId_freq.values()))
    stimulus = Phrase(phrase_id=stimulusId).getPhrase().content


    return render_template('questionnaire.html', error=error, form=form, stimulus=stimulus, packId=packId)


def getUnseenPhraseIdList(packId):
    pack = Pack(pack_id=packId).getPack()
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in
                                  PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(pack.questionnaire_id)]
    packList = Pack.getPackList_byUserId(pack.user_id)
    phraseIdList_byUser = []
    for pack in packList:
        phraseIdList_byUser.extend(
            [response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if item not in phraseIdList_byUser]
    return unseenPhraseIdList