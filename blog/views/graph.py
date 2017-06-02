from blog.models.db_config import *
from flask import render_template, Blueprint, request, jsonify, session
from blog import app
from blog.views.permission_config import user
import json
import time

graph_page = Blueprint('graph', __name__, template_folder='templates')


@app.route('/graph')
@user.require(http_exception=403)
def graph():
    tagGraphList = Graph().getGraphList_bySource('tags')
    responseGraphList = Graph().getGraphList_bySource('responses')
    tagAndResponseGraphList = Graph().getGraphList_bySource('tagsAndResponses')

    return render_template('graphViz.html',
                           tagGraphList=tagGraphList,
                           responseGraphList=responseGraphList,
                           tagAndResponseGraphList=tagAndResponseGraphList)


@app.route('/getNodes', methods=['POST'])
@user.require(http_exception=403)
def getNodes():
    graphId = request.json['graphId']
    nodeList = []
    for nodeInGraph in NodeInGraph().getNodes_byGraphId(graphId):
        nodeList.append({
            'content': Phrase(nodeInGraph.phrase_id).getPhrase().content,
            'id': nodeInGraph.phrase_id
        })

    nodeList = sorted(nodeList, key=lambda k: k['content'].__len__())

    return jsonify({'nodeList': nodeList})


@app.route('/getGraph', methods=['POST'])
@user.require(http_exception=403)
def getGraph():

    graphId = request.json['graphId']
    nodeIdList = [int(id) for id in request.json['nodeIdList']]
    level = int(request.json['level'])

    user_id = User(username=session['username']).getUser().id
    for node in nodeIdList:
        SearchedPhrase(
            user_id=user_id,
            phrase_id=node,
            time=time.strftime('%Y-%m-%d %H:%M:%S')).addIfNotExists()


    edgeInGraphList = []
    nodeInGraphIdList = set(nodeIdList)
    for i in range(level):
        edgeInGraphList.extend(EdgeInGraph().getEgoNet_byGraphId(graph_id=graphId, nodeIdList=nodeInGraphIdList))
        for edge in edgeInGraphList:
            nodeInGraphIdList.add(edge.phrase1_id)
            nodeInGraphIdList.add(edge.phrase2_id)

    nodeInGraphList = NodeInGraph().getNodes_byNodeIdList(graph_id=graphId, nodeInGraphIdList=nodeInGraphIdList)

    return getGraphFile(nodeInGraphList, edgeInGraphList, nodeIdList)


def getGraphFile(nodeInGraphList, edgeInGraphList, nodeIdList):

    final_source = []
    final_dest = []
    final_weight = []

    for edge in edgeInGraphList:
        final_source.append(edge.phrase1_id)
        final_dest.append(edge.phrase2_id)
        final_weight.append(edge.weight)

    list_node = []
    dic_node = {}
    for node in nodeInGraphList:
        dic_node['name'] = node.phrase_id
        dic_node['content'] = Phrase(phrase_id=node.phrase_id).getPhrase().content
        dic_node['size'] = node.weight
        if dic_node['name'] in nodeIdList:
            dic_node['color'] = 'pink'
        else:
            dic_node['color'] = 'LightSkyBlue'
        list_node.append(dic_node.copy())

    list_edge = []
    dic_edge = {}
    for count, item in enumerate(final_source):
        dic_edge['source'] = item
        dic_edge['target'] = final_dest[count]
        dic_edge['weight'] = final_weight[count]
        list_edge.append(dic_edge.copy())

    final_dic = {}
    final_dic['nodes'] = list_node
    final_dic['links'] = list_edge

    graphFile = json.dumps(final_dic)

    # print(graphFile)

    return graphFile