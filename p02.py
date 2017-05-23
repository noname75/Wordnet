import os

from blog import app


app.secret_key = os.urandom(24)
app.run(debug=True)

