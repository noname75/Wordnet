from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *

graphManagement_page = Blueprint('graphManagement', __name__, template_folder='templates')


@app.route('/graphManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def graphManagement():
    return render_template('graphManagement.html')
