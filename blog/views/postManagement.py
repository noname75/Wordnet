from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *
import json
import time
from collections import Counter
import re

postManagement_page = Blueprint('postManagement', __name__, template_folder='templates')


@app.route('/postManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def postManagement():

    return render_template('postManagement.html')


@app.route('/addPost', methods=['POST'])
@admin.require(http_exception=403)
def addPost():
    blackList = PhraseController().getBlackPhrases()
    blackList = [e[0] for e in blackList]
    if request.method == 'POST':
        file = request.files['file']
        if file.filename[-5:] == '.json':
            data = file.stream.read().decode("utf-8")
            postList = json.loads(data)
            i = 0
            for post in postList:
                if not isExistsBlackPhrase(blackList, post['caption']):
                    phrase_id = Phrase(content=post['name']).addIfNotExists().id
                    Post(
                        code=post['code'],
                        caption=post['caption'],
                        publishTime=post['time'],
                        storeTime=time.strftime('%Y-%m-%d %H:%M:%S'),
                        uid=post['uid'],
                        phrase_id=phrase_id
                    ).addIfNotExists()
                i = i + 1
                if i % 1000 == 0:
                    print(i, ' / ', postList.__len__())

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

    # postCountGroupByPublishTime
    labels = []
    data = []
    for row in Post().getCountGroupByPublishTime():
        count = row.count
        year_month = str(row.year) + '.' + str(row.month)
        labels.append(year_month)
        data.append(count)
    finalData['postCountGroupByPublishTime'] = {'labels': labels, 'data': data}


    # postCountGroupByStoreTime
    labels = []
    data = []
    for row in Post().getCountGroupByStoreTime():
        count = row.count
        year_month = str(row.year) + '.' + str(row.month)
        labels.append(year_month)
        data.append(count)
    finalData['postCountGroupByStoreTime'] = {'labels': labels, 'data': data}


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


def isExistsBlackPhrase(blackList, caption):
    tagList = re.compile("(#\\w+)").findall(caption)
    for tag in tagList:
        if tag[1:] in blackList:
            return True
    return False