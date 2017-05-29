from flask import render_template, Blueprint, request, flash, redirect, url_for
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import admin
from blog.forms.AddQuestionnaireForm import AddQuestionnaireForm

addQuestionnaire_page = Blueprint('addQuestionnaire', __name__, template_folder='templates')


@app.route('/addQuestionnaire', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def addQuestionnaire():
    form = AddQuestionnaireForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():

        questionnaire = Questionnaire(
            subject=form.subject.data,
            moreInfo=form.moreInfo.data
        ).addQuestionnaire()

        stimuliList = form.stimuli.data.split('\n')

        for s in stimuliList:
            stimulus = Phrase(content=s).addIfNotExists()
            PhraseInQuestionnaire(
                phrase_id=stimulus.id,
                questionnarire_id=questionnaire.id).addPhraseInQuestionnaire()

        flash(message='پرسش‌نامه ثبت شد.', category='success')
        return redirect(url_for('questionnaireList', isChosen=0))

    return render_template('addQuestionnaire.html', error=error, form=form)
