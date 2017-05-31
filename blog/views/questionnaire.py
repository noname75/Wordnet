from flask import render_template, Blueprint, request, session, url_for
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user
import time

questionnaire_page = Blueprint('questionnaire', __name__, template_folder='templates')


@app.route('/questionnaire/<int:questionnaire_id>', methods=['GET'])
@user.require(http_exception=403)
def questionnaire(questionnaire_id):
    questionnaire = Questionnaire(questionnaire_id=questionnaire_id).getQuestionnaire()

    # Set number of users which where participated in this questionnaire
    packList = Pack.getPackList_byQuestionnaireId(questionnaire.id)
    userList = set()
    for pack in packList:
        userList.add(pack.user_id)
    questionnaire.userNumber = len(userList)

    #set existUnansweredPicture
    user_id = User(session['username']).getUser().id
    questionnaire.isExistUnansweredPicture = existUnansweredPicture(user_id, questionnaire_id)


    return render_template('questionnaire.html', questionnaire=questionnaire)


@app.route("/addPack", methods=['POST'])
@user.require(http_exception=403)
def addPack():
    questionnaireId = int(request.json['questionnaireId'])
    isChosen = bool(int(request.json['isChosen']))
    isPictorial = bool(int(request.json['isPictorial']))

    questionnaire = Questionnaire(questionnaire_id=questionnaireId).getQuestionnaire()

    if not questionnaire.isActive or not questionnaire.isChosen == isChosen or (
                isPictorial and not questionnaire.isPictorial):
        raise AssertionError()

    pack = Pack(
        questionnaire_id=questionnaireId,
        user_id=User(session['username']).getUser().id,
        startTime=time.strftime('%Y-%m-%d %H:%M:%S'),
        isPictorial=isPictorial,
        isChosen=isChosen)

    pack.addPack()

    return url_for('pack', packId=pack.id)


def existUnansweredPicture(user_id, questionnaire_id):
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in
                                  PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(questionnaire_id)]
    packList = Pack.getPackList_byQuestionnaireIdAndUserId(questionnaire_id, user_id)
    phraseIdList_byUser = []
    for pack in packList:
        phraseIdList_byUser.extend(
            [response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if
                          (item not in phraseIdList_byUser) and PictureForPhrase(phrase_id=item,
                                                                                 questionnaire_id=pack.questionnaire_id).getPicture()]
    return not (unseenPhraseIdList.__len__() == 0)