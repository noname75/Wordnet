from flask import render_template, Blueprint
from blog.models.db_config import *
from blog import app
from flask_login import login_required

profile_page = Blueprint('profile', __name__, template_folder='templates')
@app.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    user = User(username).getUser()
    return render_template('profile.html', user=user)