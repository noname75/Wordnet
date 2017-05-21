from flask import Blueprint, redirect, flash, session, url_for
from blog import app
from flask.ext.principal import identity_changed, AnonymousIdentity

logout_page = Blueprint('logout', __name__, template_folder='templates')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))