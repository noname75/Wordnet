from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User(username).getUser()
    return render_template('profile.html', user=user)