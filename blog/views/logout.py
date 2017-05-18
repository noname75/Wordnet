from flask import request, redirect, url_for, abort, render_template, flash, session
from blog.forms import *
from passlib.hash import bcrypt
from blog.models.db_config import *


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('خروج از سایت انجام شد.', category='success')
    return redirect(url_for('index'))