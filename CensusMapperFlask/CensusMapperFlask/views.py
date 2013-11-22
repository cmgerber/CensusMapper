#!../env/bin/python

from CensusMapperFlask import app
import flask

@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/create_user')
def create_user():
    return flask.render_template('create_account.html')

@app.route('/login')
def login():
    return flask.render_template('login.html')

@app.route('/map')
def map():
    return flask.render_template('main_map.html')