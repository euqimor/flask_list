from flask import Flask, render_template
import os
import sqlite3
from contextlib import closing

app = Flask(__name__)

@app.route('/')
def print_list():
    with closing(sqlite3.connect(os.environ['BOT_DB'])) as con:
        suggestions = [x[0] for x in con.execute('SELECT suggestion FROM Suggestions WHERE suggestion_type=="game";').fetchall()]
    return render_template('list.html', suggestions=suggestions)




