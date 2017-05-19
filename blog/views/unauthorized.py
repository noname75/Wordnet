from flask import Blueprint, render_template, redirect, url_for
from blog import app, login_manager

unauthorized_page = Blueprint('unauthorized_handler', __name__, template_folder='templates')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauthorized.html')