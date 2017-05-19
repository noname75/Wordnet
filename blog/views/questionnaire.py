from blog.models.db_config import *
from flask import request, render_template, Blueprint

from blog import app
from blog.forms.QuestionnaireForm import QuestionnaireForm


questionnaire_page = Blueprint('questionnaire', __name__, template_folder='templates')


@app.route('/questionnaire/<packId>', methods=['GET', 'POST'])
def questionnaire(packId):
    form = QuestionnaireForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
#         pack().addResponse(form.response.name, form.response.data,form.response)
        print(form.response.data)

    return render_template('questionnaire.html', error=error, form=form, stimulus=stimulus, packId=packId)

