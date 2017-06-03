from flask import render_template, Blueprint
from blog.models.db_config import *
from blog import app
from blog.views.permission_config import user
import time


endPack_page = Blueprint('endPack', __name__, template_folder='templates')


@app.route('/endPack/<int:pack_id>', methods=['GET'])
@user.require(http_exception=403)
def endPack(pack_id):
    pack = Pack(pack_id=pack_id).getPack()
    pack.setFinishTime(time.strftime('%Y-%m-%d %H:%M:%S'))
    pack.duration = pack.finishTime - pack.startTime
    if ResponseInPack.getResponseCount_byPackId(pack.id) != 0:
        pack.setIsChecked(False)
    pack.numberOfResponses = ResponseInPack.getResponseCount_byPackId(pack.id)

    return render_template('endPack.html', pack=pack)
