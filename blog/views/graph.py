from blog.models.db_config import *
from flask import render_template, Blueprint
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


@app.route('/showGraph/<graphId>')
@user.require(http_exception=403)
def show_graph(graphId):
    node = NodeInGraph().getNodes_byGraphId(graph_id=graphId)
    source, dest, weight = EdgeInGraph().getEdges_byGraphId(graph_id=graphId)

    final_source = []
    final_dest = []
    final_weight = []
    final_node = []

    for itm in source:
        final_source.append(itm[0])
    for itm in dest:
        final_dest.append(itm[0])
    for itm in weight:
        final_weight.append(itm[0])
    for itm in node:
        final_node.append(itm[0])

    list_node = []
    dic_node = {}
    for i in final_node:
        dic_node['name'] = i
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

    graph_file = json.dumps(final_dic, ensure_ascii=False)

    print(graph_file)

    return graph_file