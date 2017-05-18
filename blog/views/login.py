from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User(username).getUser():
            if bcrypt.verify(password, User(username).getUser().password):
                session['username'] = username
                flash(message=username +' عزیز! به سایت خوش آمدید.' , scategory='success')
            else:
                error = 'رمز عبور صحیح نیست.'
                flash(message='ورود ناموفق', category='warning')
        else:
            error = 'کاربری با این نام وجود ندارد.'
            flash(message='ورود ناموفق', category='warning')

    return render_template('index.html', error=error)