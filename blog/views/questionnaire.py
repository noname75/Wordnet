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
    try:

        pack = Pack(pack_id=packId).getPack()
        if User(user_id=pack.user_id).username != session['username']:
            redirect('authorisation_failed')

        packResponseCount = ResponseInPack.getResponseList_byPackId(pack.id).__len__()
        if packResponseCount >= config.STIMULUS_COUNT:
            pack.setFinishTime(time.strftime('%Y-%m-%d %H:%M:%S'))
            flash(message='پرسشنامه با موفقیت تکمیل شد. ممنون از مشارکت شما.', category='success')
            return redirect('/')

        unseenPhraseIdList = getUnseenPhraseIdList(pack.id)
        if unseenPhraseIdList.__len__() == 0:
            raise AssertionError()

        form = QuestionnaireForm(request.form)
        stimulus = Phrase(phrase_id=random.choice(unseenPhraseIdList)).getPhrase().content

        return render_template('questionnaire.html', form=form, stimulus=stimulus, packId=packId)

    except Exception:
        return redirect('page_not_found')


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