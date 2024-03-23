#!/usr/bin/python3
""" A script that starts a web app using storage for fetching data from engine
Routes:
    /states_list: display a HTML page inside tag BODY
    H1: States
    UL: with the list of all State objects in present DB
        LI: description of one State: <state.id>: <B><state.name><B>
"""
from flask import Flask, render_template
from models import storage, State


app = Flask(__name__)
@app.route('/states_list', strict_slashes=False)
def states_list():
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
