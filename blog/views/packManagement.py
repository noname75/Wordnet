from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *

packManagement_page = Blueprint('packManagement', __name__, template_folder='templates')


@app.route('/packManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def packManagement():
    return render_template('packManagement.html')