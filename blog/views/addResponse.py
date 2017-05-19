from blog.models.db_config import *
from flask import request, render_template, Blueprint, session, redirect, flash, url_for
from blog import app
from blog.forms.QuestionnaireForm import QuestionnaireForm
from blog.views.permission_config import user

addResponse_page = Blueprint('addResponse', __name__, template_folder='templates')


@app.route('/addResponse/<packId>/<stimulus>', methods=['GET', 'POST'])
@user.require(http_exception=403)
def addResponse(packId, stimulus):
    form = QuestionnaireForm(request.form)

    if request.method == 'POST':

        response = Phrase(content=form.response.data).getPhrase_byContent()
        if not response:
            response = Phrase(content=form.response.data).addPhrase()

        ResponseInPack(pack_id=packId,
                       phrase1_id=Phrase(content=stimulus).getPhrase_byContent().id,
                       phrase2_id=response.id,
                       duration=10).addResponseInPack()

    return redirect(request.referrer)
