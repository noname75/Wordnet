from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *


@app.route('/test')
def test():
    getUnseenPhraseList(5)
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User(username).getUser():
            if bcrypt.verify(password, User(username).getUser().password):
                session['username'] = username
                flash(message=username + ' عزیز! به سایت خوش آمدید.', category='success')
            else:
                error = 'رمز عبور صحیح نیست.'
                flash(message='ورود ناموفق', category='warning')
        else:
            error = 'کاربری با این نام وجود ندارد.'
            flash(message='ورود ناموفق', category='warning')

    return render_template('index.html', error=error)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('خروج از سایت انجام شد.', category='success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        User(
            username=form.username.data,
            password=bcrypt.encrypt(form.password.data),
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data
        ).addUser()
        flash(message='ثبت نام شما انجام شد.', category='success')
        return render_template("index.html")

    return render_template('register.html', error=error, form=form)



@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User(username).getUser()
    return render_template('profile.html', user=user)



@app.route('/packfilling/<packId>', methods=['GET', 'POST'])
def packfilling(packId):

    form = ResponseForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
#         pack().addResponse(form.response.name, form.response.data,form.response)
        print(form.response.data)
    
        
    return render_template('questionnaire.html', error=error, form=form,stimulus=stimulus)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def getUnseenPhraseList(packId):
    pack = Pack(packId).getPack()
    phraseList_byQuestionnaire = [phrase.phrase_id for phrase in PhraseInQuestionnaire.getPhraseList_byQuestionnaireId(pack.questionnaire_id)]
    packList = Pack.getPackList_byUserId(pack.user_id)
    phraseIdList_byUser = []
    for pack in packList:
        phraseIdList_byUser.extend([response.phrase1_id for response in ResponseInPack.getResponseList_byPackId(pack.id)])
    unseenPhraseIdList = [item for item in phraseList_byQuestionnaire if item not in phraseIdList_byUser]
    for phraseId in unseenPhraseIdList:
        print(phraseId, ResponseInPack.getResponseCount_byPhraseId(phraseId))