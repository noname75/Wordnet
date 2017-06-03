from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *
from datetime import datetime

packManagement_page = Blueprint('packManagement', __name__, template_folder='templates')


@app.route('/packManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def packManagement():
    uncheckedPackList = Pack().getPackList_byIsChecked(False)
    checkedPackList = Pack().getPackList_byIsChecked(True)

    for pack in uncheckedPackList + checkedPackList:
        pack.responseCount = ResponseInPack.getResponseCount_byPackId(pack.id)
        pack.subject = Questionnaire(questionnaire_id=pack.questionnaire_id).getQuestionnaire().subject
        pack.time = timesince(pack.startTime)

    return render_template('packManagement.html', uncheckedPackList=uncheckedPackList, checkedPackList=checkedPackList)


@app.route('/getResponseList', methods=['POST'])
@admin.require(http_exception=403)
def getResponseList():
    packId = request.json['packId']
    pack = Pack(pack_id=packId).getPack()
    responseInPackList = ResponseInPack.getResponseList_byPackId(packId)
    stimulusResponseList = []
    for responseInPack in responseInPackList:
        stimulus = Phrase(phrase_id=responseInPack.phrase1_id).getPhrase()
        response = Phrase(phrase_id=responseInPack.phrase2_id).getPhrase()
        if response:
            suggestedStatus = 'none'
            phraseController = PhraseController(phrase_id=response.id).getPhraseController()
            if phraseController:
                if phraseController.type == 'black':
                    suggestedStatus = 'rejected'
                elif phraseController.type == 'white':
                    suggestedStatus = 'accepted'
            stimulusResponseList.append(
                {'stimulus': stimulus.content,
                 'stimulusId': stimulus.id,
                 'response': response.content,
                 'responseId': response.id,
                 'status': suggestedStatus,
                 'suggestedStatus': suggestedStatus})
            stimulusResponseList.sort(key=lambda x: (x['status']))
    return jsonify({'stimulusResponseList': stimulusResponseList, 'pack_isChecked': pack.isChecked})


@app.route('/addPhraseController', methods=['POST'])
@admin.require(http_exception=403)
def addPhraseController():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file.filename[-4:] == '.txt':
                data = file.read().decode('utf8')
                for line in data.split('\r\n'):
                    content = line.split('\t')
                    phrase = Phrase(content=content[0]).addIfNotExists()
                    if content[1] == '1':
                        type = 'white'
                    elif content[1] == '0':
                        type = 'black'
                    phraseController = PhraseController(phrase_id=phrase.id, type=type)
                    last = phraseController.getPhraseController()
                    if not last:
                        phraseController.addPhraseController()
                    else:
                        if last.credit == 0:
                            last.updateType(phraseController.type)
            return ''
    except():
        pass


@app.route('/setResponseStatus', methods=['POST'])
@admin.require(http_exception=403)
def setResponseStatus():
    stimulusResponseList = request.json['stimulusResponseList']
    packId = request.json['packId']
    for stimulusResponse in stimulusResponseList:
        stimulusId = stimulusResponse['stimulusId']
        responseId = stimulusResponse['responseId']
        status = stimulusResponse['status']
        suggestedStatus = stimulusResponse['suggestedStatus']
        if status == 'accepted':
            newType = 'white'
        else:
            newType = 'black'
        if suggestedStatus == 'none':
            PhraseController(phrase_id=responseId, type=newType).addPhraseController()
        elif suggestedStatus == status:
            PhraseController(phrase_id=responseId).getPhraseController().creditPlusOne()
        else:
            PhraseController(phrase_id=responseId).getPhraseController().updateType(newType)
        ResponseInPack(pack_id=packId, phrase1_id=stimulusId, phrase2_id=responseId).getResponseInPack().setStatus(
            status)
        Pack(pack_id=packId).getPack().setIsChecked(True)

    return ''



def timesince(dt, default="همین الان"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    now = datetime.now()
    diff = now - dt

    periods = (
        (diff.days / 365, "سال"),
        (diff.days / 30, "ماه"),
        (diff.days / 7, "هفته"),
        (diff.days, "روز"),
        (diff.seconds / 3600, "ساعت"),
        (diff.seconds / 60, "دقیقه"),
        (diff.seconds, "ثانیه"),
    )

    for period, name in periods:

        if period >= 1:
            return "%d %s پیش" % (period, name)

    return default
