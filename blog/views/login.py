from flask import request, render_template, flash, session, Blueprint, redirect
from passlib.hash import bcrypt
from blog.models.db_config import *
from blog import app
from flask.ext.principal import Identity, identity_changed

login_page = Blueprint('login', __name__, template_folder='templates')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username).getUser()
        if user:
            if bcrypt.verify(password, user.password):
                session['username'] = user.username
                identity_changed.send(app, identity=Identity(id=user.id, auth_type=user.role))
                return redirect('/')
            else:
                error = 'رمز عبور صحیح نیست.'
                flash(message='ورود ناموفق', category='warning')
        else:
            error = 'کاربری با این نام وجود ندارد.'
            flash(message='ورود ناموفق', category='warning')

    return render_template('index.html', error=error)