from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *


@app.route('/test')
def test():
    print(getUnseenPhraseListWithFreq(5))
    return render_template('index.html')