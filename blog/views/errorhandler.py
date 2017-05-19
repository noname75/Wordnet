from flask import Blueprint, render_template, g
from blog import app

errorhandler_page = Blueprint('errorhandler', __name__, template_folder='templates')


@app.errorhandler(403)
def authorisation_failed(e):
    role = g.identity.auth_type
    if role == 'user':
        message = 'دسترسی به صفحه مسدود است.'
    else:
        message = 'ابتدا به سایت وارد شوید.'
    return render_template('errorhandler.html', message=message), 403


@app.errorhandler(404)
def page_not_found(e):
    message = 'صفحه یافت نشد.'
    return render_template('errorhandler.html', message=message), 404