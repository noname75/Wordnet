from flask import Blueprint, render_template, redirect, url_for
from blog import app, login_manager

error404_page = Blueprint('error404', __name__, template_folder='templates')


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404

