from flask import request, render_template, Blueprint

from blog.models.db_config import *
from blog import app


questionnaire_page = Blueprint('questionnaire_page', __name__, template_folder='templates')


@app.route('/questionnaire/<packId>', methods=['GET', 'POST'])
def packfilling(packId):
    phraseId_freq = getUnseenPhraseListWithFreq(packId)
    phraseId = np.random.choice(phraseId.keys(), 1, p=normalize(phraseId_freq.values()))
    phrase = Phrase(phraseId).getPhrase()

    form = QuestionnaireForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
#         pack().addResponse(form.response.name, form.response.data,form.response)
        print(form.response.data)

    return render_template('questionnaire.html', error=error, form=form, pharse=phrase)


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


def normalize(list):
    list = [1 / (member + 1) for member in list]
    return [member / list.sum() for member in list]