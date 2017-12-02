from flask import Flask, render_template
import os
import sqlite3
from contextlib import closing
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)

file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)



@app.route('/')
def print_list():
    with closing(sqlite3.connect(os.environ['BOT_DasdB'])) as con:
        suggestions = [x[0] for x in con.execute('SELECT suggestion FROM Suggestions WHERE suggestion_type=="game";').fetchall()]
    return render_template('list.html', suggestions=suggestions)

@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return 'error_handler'
    # return render_template('500.html'), 500

