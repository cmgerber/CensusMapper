#!../env/bin/python

from CensusMapperFlask import app
import flask

@app.route('/')
def test():
    return flask.render_template('create_account.html')