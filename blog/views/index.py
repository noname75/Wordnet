from flask import Blueprint, render_template
from blog import app

index_page = Blueprint('index', __name__, template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')
