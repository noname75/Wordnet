from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404