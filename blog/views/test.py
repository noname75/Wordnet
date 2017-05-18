from flask import render_template, Blueprint

from blog import app


test_page = Blueprint('test_page', __name__, template_folder='templates')
@app.route('/test')
def test():
    return render_template('index.html')