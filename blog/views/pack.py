from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *

@app.route('/pack/<packId>', methods=['GET', 'POST'])
def packfilling(packId):



    # np.random.choice(, 3, replace=False, p=[0.1, 0, 0.3, 0.6, 0])
    form = ResponseForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
#         pack().addResponse(form.response.name, form.response.data,form.response)
        print(form.response.data)
    
        
    return render_template('questionnaire.html', error=error, form=form,stimulus=stimulus)


def getUnseenPhraseListWithFreq(packId):
    phraseId_freq = {}
    pack = Pack(packId).getPack()
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(pack.questionnaire_id)]
    packList = Pack.getPackList_byUserId(pack.user_id)
    phraseIdList_byUser = []
    for pack in packList:
        phraseIdList_byUser.extend([response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if item not in phraseIdList_byUser]
    for phraseId in unseenPhraseIdList:
        phraseId_freq[phraseId] = ResponseInPack.getResponseCount_byPhraseId(phraseId)
    return phraseId_freq


