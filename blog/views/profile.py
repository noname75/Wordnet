from flask import render_template, Blueprint

from blog.models.db_config import *
from blog import app


profile_page = Blueprint('profile_page', __name__, template_folder='templates')
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User(username).getUser()
    return render_template('profile.html', user=user)