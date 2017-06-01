from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *
import json
import time
from collections import Counter

postManagement_page = Blueprint('postManagement', __name__, template_folder='templates')


@app.route('/postManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def postManagement():

    return render_template('postManagement.html')


@app.route('/addPost', methods=['POST'])
@admin.require(http_exception=403)
def addPost():

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


@app.route('/getPostChartsData', methods=['POST'])
@admin.require(http_exception=403)
def getPostChartsData():
    finalData = {}

    # postCountGroupByPhraseId
    labels = []
    data = []
    for row in Post().getCountGroupByPhraseId():
        phrase = Phrase(phrase_id=row.phrase_id).getPhrase().content
        if len(phrase) > 15:
            phrase = phrase[:15] + '...'
        count = row.count
        labels.append(phrase)
        data.append(count)
    finalData['postCountGroupByPharseId'] = {'labels': labels, 'data': data}

    # postCountGroupByTime
    labels = []
    data = []
    for row in Post().getCountGroupByTime():
        count = row.count
        year_month = str(row.year) + '.' + str(row.month)
        labels.append(year_month)
        data.append(count)
    finalData['postCountGroupByTime'] = {'labels': labels, 'data': data}


    # postCountGroupByUid
    counts = []
    data = []
    for row in Post().getCountGroupByUid():
        counts.append(row.count)
    counter = Counter(counts)
    for k in counter.keys():
        if counter[k] > 5:
            data.append({'x': k, 'y': counter[k]})
    finalData['postCountGroupByUid'] = {'data': data}


    # basicStatistics
    countOfPosts = Post().getCountOfPosts()
    countOfUids = Post().getCountOfUids()
    countOfPhrases = Post().getCountOfPhrases()
    finalData['basicStatistics'] = {
        'countOfPosts': countOfPosts,
        'countOfUids': countOfUids,
        'countOfPhrases': countOfPhrases
    }

    return jsonify(finalData)