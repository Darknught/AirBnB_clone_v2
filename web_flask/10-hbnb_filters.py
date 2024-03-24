#!/usr/bin/python3
""" A script that starts a web flask app
Routes:
    /hbnb_filters: display a HTML page for previous web_static proj
"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ Returns the HTML page using render_template"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('10-hbnb_filters.html',
            states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLALchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
