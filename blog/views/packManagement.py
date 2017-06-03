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

    for pack in uncheckedPackList:
        pack.responseCount = ResponseInPack.getResponseCount_byPackId(pack.id)
        pack.subject = Questionnaire(questionnaire_id=pack.questionnaire_id).getQuestionnaire().subject
        pack.time = timesince(pack.startTime)

    return render_template('packManagement.html', uncheckedPackList=uncheckedPackList, checkedPackList=checkedPackList)


@app.route('/getResponseList', methods=['POST'])
@admin.require(http_exception=403)
def getResponseList():
    packId = request.json['packId']
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
                    suggestedStatus = 'red'
                elif phraseController.type == 'white':
                    suggestedStatus = 'green'
            stimulusResponseList.append(
                {'stimulus': stimulus.content, 'response': response.content, 'suggestedStatus': suggestedStatus})
    return jsonify({'stimulusResponseList': stimulusResponseList})


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
                    if not phraseController.getPhraseController():
                        phraseController.addPhraseController()
                    else:
                        if phraseController.credit == 0:
                            phraseController.updateType()
            return ''
    except():
        pass


def timesince(dt, default="همین الان"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, "سال", "سال"),
        (diff.days / 30, "ماه", "ماه"),
        (diff.days / 7, "هفته", "هفته"),
        (diff.days, "روز", "روز"),
        (diff.seconds / 3600, "ساعت", "ساعت"),
        (diff.seconds / 60, "دقیقه", "دقیقه"),
        (diff.seconds, "ثانیه", "ثاینه"),
    )

    for period, singular, plural in periods:

        if period >= 1:
            return "%d %s پیش" % (period, singular if period == 1 else plural)

    return default
