from flask import Flask

app = Flask(__name__)

from blog.views.errorhandler import errorhandler_page
from blog.views.index import index_page
from blog.views.login import login_page
from blog.views.logout import logout_page
from blog.views.profile import profile_page
from blog.views.questionnaire import questionnaire_page
from blog.views.register import register_page
from blog.views.questionnaireList import questionnaireList_page
from blog.views.addQuestionnaire import addQuestionnaire_page
from blog.views.graph import graph_page
from blog.views.editQuestionnaire import editQuestionnaire_page
from blog.views.pack import pack_page
from blog.views.endPack import endPack_page
from blog.views.postManagement import postManagement_page
from blog.views.graphManagement import graphManagement_page

app.register_blueprint(errorhandler_page)
app.register_blueprint(index_page)
app.register_blueprint(login_page)
app.register_blueprint(logout_page)
app.register_blueprint(profile_page)
app.register_blueprint(register_page)
app.register_blueprint(questionnaire_page)
app.register_blueprint(questionnaireList_page)
app.register_blueprint(graph_page)
app.register_blueprint(editQuestionnaire_page)
app.register_blueprint(pack_page)
app.register_blueprint(endPack_page)
app.register_blueprint(postManagement_page)
app.register_blueprint(graphManagement_page)


# from blog.models.db_config import *
#
# with open('edges_di_10_0_0.4.txt', 'r', encoding='utf-8-sig') as file:
# for line in file:
#         edge = line[:-2].split(' ')
#         source = edge[0]
#         target = edge[1]
#         weight = float(edge[2])
#
#         print(source, target)
#         source = Phrase(content=source).addIfNotExists()
#         target = Phrase(content=target).addIfNotExists()
#
#         node = NodeInGraph(
#             graph_id=2,
#             phrase_id=source.id,
#             weight=1
#         )
#         if not db.session.query(NodeInGraph).filter_by(graph_id=node.graph_id,phrase_id=node.phrase_id).first():
#             db.session.add(node)
#             db.session.commit()
#         node = NodeInGraph(
#             graph_id=2,
#             phrase_id=target.id,
#             weight=1
#         )
#         if not db.session.query(NodeInGraph).filter_by(graph_id=node.graph_id,phrase_id=node.phrase_id).first():
#             db.session.add(node)
#             db.session.commit()
#
#         edge = EdgeInGraph(
#             graph_id=2,
#             phrase1_id=source.id,
#             phrase2_id=target.id,
#             weight=weight
#         )
#         if not db.session.query(EdgeInGraph).filter_by(graph_id=edge.graph_id,phrase1_id=edge.phrase1_id,phrase2_id=edge.phrase2_id).first():
#             db.session.add(edge)
#             db.session.commit()