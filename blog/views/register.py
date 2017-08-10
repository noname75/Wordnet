from flask import request, render_template, flash, Blueprint, redirect, url_for, session
from passlib.hash import bcrypt
from blog.forms.RegisterationForm import RegistrationForm
from blog.models.db_config import *
from blog import app
from flask.ext.principal import Identity, identity_changed
import time

register_page = Blueprint('register', __name__, template_folder='templates')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            password=bcrypt.encrypt(form.password.data),
            firstname=form.firstname.data,
            birthyear=form.birthyear.data,
            email=form.email.data,
            registerationTime=time.strftime('%Y-%m-%d %H:%M:%S')
        ).addUser()
        session['username'] = user.username
        if user.role == 'admin':
            session['admin'] = True
        identity_changed.send(app, identity=Identity(id=user.id, auth_type=user.role))
        return redirect('/')

    return render_template('register.html', error=error, form=form)