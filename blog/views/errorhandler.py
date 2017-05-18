from flask import Blueprint, render_template

from blog import app


error404_page = Blueprint('error404_page', __name__, template_folder='templates')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404