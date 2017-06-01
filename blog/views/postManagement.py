from flask import render_template, Blueprint, request
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *
import json
import time
from werkzeug.datastructures import FileStorage

postManagement_page = Blueprint('postManagement', __name__, template_folder='templates')


@app.route('/postManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def postManagement():
    return render_template('postManagement.html')


@app.route('/addPost', methods=['POST'])
@admin.require(http_exception=403)
def addPost():
    # code = request.json['code']
    # caption = request.json['caption']
    # publishTime = request.json['time']
    # uid = request.json['uid']
    # phrase_id = Phrase(content=request.json['name'], creationTime=time.strftime('%Y-%m-%d %H:%M:%S')).addIfNotExists().id
    #
    # Post(
    # code=code,
    #     caption=caption,
    #     publishTime=publishTime,
    #     storeTime=time.strftime('%Y-%m-%d %H:%M:%S'),
    #     uid=uid,
    #     phrase_id=phrase_id
    # ).addIfNotExists()

    if request.method == 'POST':
        file = request.files['file']
        if file.filename[-5:] == '.json':
            data = file.stream.read().decode("utf-8")
            postList = json.loads(data)
            for post in postList:
                phrase_id = Phrase(content=post['name'],
                                   creationTime=time.strftime('%Y-%m-%d %H:%M:%S')).addIfNotExists().id
                Post(
                    code=post['code'],
                    caption=post['caption'],
                    publishTime=post['time'],
                    storeTime=time.strftime('%Y-%m-%d %H:%M:%S'),
                    uid=post['uid'],
                    phrase_id=phrase_id
                ).addIfNotExists()

    return ''