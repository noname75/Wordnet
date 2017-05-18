from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *

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