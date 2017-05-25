from blog.models.db_config import *
from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import user
import json

graph_page = Blueprint('graph', __name__, template_folder='templates')


@app.route('/graph')
@user.require(http_exception=403)
def graph():
    tagGraphList = Graph().getGraphList_bySource('tags')
    responseGraphList = Graph().getGraphList_bySource('responses')
    tagAndResponseGraphList = Graph().getGraphList_bySource('tagsAndResponses')

    return render_template('graph.html',
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
    return jsonify({'nodeList': nodeList})


@app.route('/getGraph', methods=['POST'])
@user.require(http_exception=403)
def getGraph():
    graphId = request.json['graphId']
    nodeIdList = [int(id) for id in request.json['nodeIdList']]

    edgeInGraphList = EdgeInGraph().getEgoNet_byGraphId(graph_id=graphId, nodeIdList=nodeIdList)

    return getGraphFile(edgeInGraphList)


def getGraphFile(edgeInGraphList):

    final_source = []
    final_dest = []
    final_weight = []

    for edge in edgeInGraphList:
        final_source.append(edge.phrase1_id)
        final_dest.append(edge.phrase2_id)
        final_weight.append(edge.weight)

    final_node = list(set(final_source) | set(final_dest))

    list_node = []
    dic_node = {}
    for i in final_node:
        dic_node['name'] = i
        dic_node['content'] = Phrase(phrase_id=i).getPhrase().content
        dic_node['group'] = 1
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

    return graphFile