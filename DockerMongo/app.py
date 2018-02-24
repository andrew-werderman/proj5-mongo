import os
import flask
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging

app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

client = MongoClient("db", 27017)
db = client.tododb

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return render_template('calc.html')

@app.route('/todo')
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return render_template('404.html'), 404

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")

    # Get input values 
    km = request.args.get('km', 999, type=float)
    brev_dist_km = request.args.get('brev_dist_km', 300, type=int)
    start_date = request.args.get('start_date', '2018-01-19', type=str)
    start_time = request.args.get('start_time', '16:00:00', type=str)

    # Combine date/time into correct format
    dateTime = '{} {}'.format(start_date, start_time)
    brev_start_time = arrow.get(dateTime, 'YYYY-MM-DD HH:mm')
    
    open_time = acp_times.open_time(km, brev_dist_km, brev_start_time)
    close_time = acp_times.close_time(km, brev_dist_km, brev_start_time)
    result = {"open": open_time.for_json(), "close": close_time.for_json()}
    return flask.jsonify(result=result)

#############

@app.route('/new', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))


app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(host='0.0.0.0', port=CONFIG.PORT, debug=True)
