from flask import render_template, Blueprint
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user


profile_page = Blueprint('profile', __name__, template_folder='templates')

@app.route('/profile/<username>', methods=['GET'])
@user.require(http_exception=403)
def profile(username):
    user = User(username).getUser()
    return render_template('profile.html', user=user)