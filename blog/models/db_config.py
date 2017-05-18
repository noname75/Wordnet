from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from blog import app


app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://localhost\SQLExpress/wordnet?driver=ODBC+Driver+11+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


