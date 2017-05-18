from flask import request, redirect, url_for, abort, render_template, flash,session
from blog.models import *
from blog.forms import *
import random
from passlib.hash import bcrypt


@app.route('/test')
def test():
    getUnseenPhraseList(6)
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
                flash(message=username + ' عزیز! به سایت خوش آمدید.',category='success')
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
    user = User(username)
    return render_template('profile.html', user=user)



@app.route('/packfilling/<packId>', methods=['GET', 'POST'])
def packfilling(packId):




    form = ResponseForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
#         pack().addResponse(form.response.name, form.response.data,form.response)
        print(form.response.data)
    
        
    return render_template('questionnaire.html', error=error, form=form,stimulus=stimulus)



