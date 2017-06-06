from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *
from datetime import datetime
import networkx as nx
import re
import math


graphManagement_page = Blueprint('graphManagement', __name__, template_folder='templates')


@app.route('/graphManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def graphManagement():

    return render_template('graphManagement.html')


@app.route('/getDataCount', methods=['POST'])
@admin.require(http_exception=403)
def getDataCount():
    startTime = datetime.strptime(request.json['startTime'], "%m/%d/%Y")
    finishTime = datetime.strptime(request.json['finishTime'], "%m/%d/%Y")
    timeLimitation = request.json['timeLimitation']

    if not timeLimitation:
        postCount = Post().getCountOfPosts()
        responseCount = ResponseInPack().getAcceptedResponseCount()
    else:
        postCount = Post().getCountOfPosts_byStartTimeAndFinishTime(startTime, finishTime)
        responseCount = ResponseInPack().getAcceptedResponseCount_byStartTimeAndFinishTime(startTime, finishTime)

    return jsonify({'postCount': postCount, 'responseCount': responseCount})


@app.route('/calculateGraph', methods=['POST'])
@admin.require(http_exception=403)
def calculateGraph():
    startTime = datetime.strptime(request.json['startTime'], "%m/%d/%Y")
    finishTime = datetime.strptime(request.json['finishTime'], "%m/%d/%Y")
    timeLimitation = request.json['timeLimitation']
    source = request.json['source']
    isDirected = request.json['isDirected']
    minUserOnNode = int(request.json['minUserOnNode'])
    minUserOnEdge = int(request.json['minUserOnEdge'])
    minEdgeWeight = float(request.json['minEdgeWeight'])

    if source == 'tags':
        posts = getTagsData(timeLimitation, startTime, finishTime)
        g = constructTagGraph(posts, isDirected, minUserOnNode, minUserOnEdge, minEdgeWeight)
    elif source == 'responses':
        responses = getResponsesData(timeLimitation, startTime, finishTime)
        g = constructResponsesGraph(responses, isDirected, minUserOnNode, minUserOnEdge, minEdgeWeight)

    return jsonify({'nodeCount': g.number_of_nodes(), 'edgeCount': g.number_of_edges()})


@app.route('/constructGraph', methods=['POST'])
@admin.require(http_exception=403)
def constructGraph():
    startTime = datetime.strptime(request.json['startTime'], "%m/%d/%Y")
    finishTime = datetime.strptime(request.json['finishTime'], "%m/%d/%Y")
    timeLimitation = request.json['timeLimitation']
    source = request.json['source']
    isDirected = request.json['isDirected']
    minUserOnNode = int(request.json['minUserOnNode'])
    minUserOnEdge = int(request.json['minUserOnEdge'])
    minEdgeWeight = float(request.json['minEdgeWeight'])
    name = request.json['name']
    moreInfo = request.json['moreInfo']

    if source == 'tags':
        posts = getTagsData(timeLimitation, startTime, finishTime)
        g = constructTagGraph(posts, isDirected, minUserOnNode, minUserOnEdge, minEdgeWeight)
    elif source == 'responses':
        responses = getResponsesData(timeLimitation, startTime, finishTime)
        g = constructResponsesGraph(responses, isDirected, minUserOnNode, minUserOnEdge, minEdgeWeight)

    return ''


def getResponsesData(timeLimitation, startTime, finishTime):
    if not timeLimitation:
        responses = ResponseInPack().getAcceptedResponses()
    else:
        responses = ResponseInPack().getAcceptedResponses_byStartTimeAndFinishTime(startTime, finishTime)

    return responses


def constructResponsesGraph(responses, isDirected, minUserOnNode, minUserOnEdge, minEdgeWeight):
    g = nx.Graph()
    for response in responses:
        source = response.phrase1_content
        target = response.phrase2_content
        uid = response.pack_id
        if not g.has_node(source):
            g.add_node(source, distUserList=[])
        if not g.has_node(target):
            g.add_node(source, distUserList=[])
        if not g.node[source]['distUserList'].__contains__(uid):
            g.node[source]['distUserList'].append(uid)

    return g


def getTagsData(timeLimitation, startTime, finishTime):
    if not timeLimitation:
        posts = Post().getPosts()
    else:
        posts = Post().getPosts_byStartTimeAndFinishTime(startTime, finishTime)

    return posts


def constructTagGraph(posts, isDirected, minUserOnNode, minUserOnEdge, minEdgeWeight):
    # Read tagGroups
    tag_pattern = re.compile("(#\\w+)")
    tagCount = 0
    tagGroups = []

    i = 0
    for post in posts:
        uid = post.uid
        tagList = tag_pattern.findall(post.caption)
        if tagList.__len__() == 0:
            continue
        tagGroup = []
        for tagContent in tagList:
            tag = Phrase(content=tagContent[1:]).addIfNotExists().id
            if not tag in tagGroup:
                tagGroup.append(tag)
        tagGroup = tuple(tagGroup)
        tagGroups.append((tagGroup, uid,))
        tagCount = tagCount + tagGroup.__len__()
        i = i + 1
        if i % 100 == 0:
            print(i, '/', posts.__len__())

    info = {}
    info["#Posts"] = posts.__len__()
    info['Average#Tags'] = tagCount / tagGroups.__len__()
    info['#TagGroups'] = tagGroups.__len__()
    printInfo(info)


    #Construct Graph
    g = nx.Graph()

    for tagGroup, uid in tagGroups:

        for source in tagGroup:
            if not g.has_node(source):
                g.add_node(source, distUserList=[])
            if not g.node[source]['distUserList'].__contains__(uid):
                g.node[source]['distUserList'].append(uid)

        for i, source in enumerate(tagGroup[:-1]):
            for distance, target in enumerate(tagGroup[i + 1:]):
                if not g.has_edge(source, target):
                    g.add_edge(source, target, weight=0, occur=0, distUserList=[])
                else:
                    if g.edge[source][target]['distUserList'].__contains__(uid):
                        continue
                g.edge[source][target]['weight'] = g.edge[source][target]['weight'] + 1 / (math.log(distance + 1) + 1)
                g.edge[source][target]['distUserList'].append(uid)

    info = {}
    info['#nodes'] = g.number_of_nodes()
    info['#edges'] = g.number_of_edges()
    printInfo(info)


    #Pruning Nodes
    for node in g.nodes():
        if g.node[node]['distUserList'].__len__() < minUserOnNode:
            g.remove_node(node)


    #Normalization
    if isDirected:
        di = nx.DiGraph()
        for node in g.nodes():
            di.add_node(node, distUserList=g.node[node]['distUserList'])
        for source, target in g.edges():
            source_distUseList_len = g.node[source]['distUserList'].__len__()
            target_distUseList_len = g.node[target]['distUserList'].__len__()
            source_target_weight = g.edge[source][target]['weight']
            di.add_edge(source, target, weight=source_target_weight / source_distUseList_len,
                        distUserList=g.edge[source][target]['distUserList'])
            di.add_edge(target, source, weight=source_target_weight / target_distUseList_len,
                        distUserList=g.edge[source][target]['distUserList'])
        g = di

    else:
        for source, target in g.edges():
            source_distUseList_len = g.node[source]['distUserList'].__len__()
            target_distUseList_len = g.node[target]['distUserList'].__len__()
            edge_distUserList_len = g.edge[source][target]['distUserList'].__len__()
            g.edge[source][target]['weight'] = g.edge[source][target]['weight'] / (
            source_distUseList_len + target_distUseList_len - edge_distUserList_len)


    #Pruning Edges
    for s, t in g.edges():
        if g.edge[s][t]['distUserList'].__len__() < minUserOnEdge or g.edge[s][t]['weight'] < minEdgeWeight:
            g.remove_edge(s, t)

    return g


def printInfo(info):
    print("_______________________INFO______________________\n")
    for i in info.keys():
        print("%30s: %d" % (i, info[i]))
    print("_________________________________________________\n")