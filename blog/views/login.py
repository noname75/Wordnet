from flask import request, render_template, flash, session, Blueprint, redirect
from passlib.hash import bcrypt

from blog.models.db_config import *
from blog import app


login_page = Blueprint('login', __name__, template_folder='templates')
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
                return redirect(request.referrer)
            else:
                error = 'رمز عبور صحیح نیست.'
                flash(message='ورود ناموفق', category='warning')
        else:
            error = 'کاربری با این نام وجود ندارد.'
            flash(message='ورود ناموفق', category='warning')

    return render_template('index.html', error=error)