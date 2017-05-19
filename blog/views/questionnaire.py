import random

from flask import request, render_template, Blueprint

from blog import app
from blog.forms.QuestionnaireForm import QuestionnaireForm


questionnaire_page = Blueprint('questionnaire', __name__, template_folder='templates')


@app.route('/questionnaire/<packId>', methods=['GET', 'POST'])
def questionnaire(packId):
    phraseId_freq = getUnseenPhraseListWithFreq(packId)
    phraseId = random.choice(list(phraseId_freq.keys()))
    # phraseId = np.random.choice(phraseId_freq.keys(), 1, p=normalize(phraseId_freq.values()))
    stimulus = Phrase(phraseId).getPhrase().content

    form = QuestionnaireForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
#         pack().addResponse(form.response.name, form.response.data,form.response)
        print(form.response.data)

    return render_template('questionnaire.html', error=error, form=form, stimulus=stimulus, packId=packId)


def getUnseenPhraseListWithFreq(packId):
    phraseId_freq = {}
    pack = Pack(packId=packId).getPack()
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(pack.questionnaire_id)]
    packList = Pack.getPackList_byUserId(pack.user_id)
    phraseIdList_byUser = []
    for pack in packList:
        phraseIdList_byUser.extend([response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if item not in phraseIdList_byUser]
    for phraseId in unseenPhraseIdList:
        phraseId_freq[phraseId] = ResponseInPack.getResponseCount_byPhraseId(phraseId)
    return phraseId_freq


def normalize(freq_list):
    inverse_freq_list = [1 / (member + 1) for member in freq_list]
    normalized_inverse_freq_list = [member / sum(inverse_freq_list) for member in inverse_freq_list]
    return normalized_inverse_freq_list