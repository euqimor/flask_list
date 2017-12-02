from flask import Flask, render_template
import os
import sqlite3
from contextlib import closing
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
from flask import request, Response

app = Flask(__name__)

file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)





def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'test1' and password == 'test2'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



@app.route('/')
@requires_auth
def print_list():
    with closing(sqlite3.connect(os.environ['BOT_DB'])) as con:
        suggestions = [x[0] for x in con.execute('SELECT suggestion FROM Suggestions WHERE suggestion_type=="game";').fetchall()]
    return render_template('list.html', suggestions=suggestions)

@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return 'HTTP 500: Internal server error', 500

