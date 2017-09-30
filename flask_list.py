from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def print_list():
    os.chdir(os.path.expanduser('~/py/discord/'))
    with open('suggestions') as f:
        suggestions = eval(f.read())
        set_of_games = set({})
        for name in suggestions:
            for game in suggestions[name]:
                set_of_games.add(game)
    return render_template('list.html', suggestions=set_of_games)




