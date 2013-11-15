#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True
db = shelve.open("shorts.db")

###
# This is what the html page should send data to
###
@app.route('/shorts', methods=['POST'])
def shorts():
        begin = "people.ischool.berkeley.edu/~mrobison/server/short/"
        longURL = str(request.form['long'])
        longURL = processURL(longURL)
        shortURL = str(request.form['short'])
        db[shortURL] = longURL
        return home(begin+shortURL)

###
# Redirection:
###
@app.route('/short/<shortURL>')
def short(shortURL):
        shortURL = str(shortURL)
        if(db.has_key(shortURL)==False):
                return render_template('page_not_found.html'), 404
        longURL = db[shortURL]
        return flask.redirect(longURL)
        #redirect to whatever long URL is associated

@app.route('/')
def home(newURL="default"):
        if newURL=="default":
                return flask.render_template('proj1.html')
        else:
                return flask.render_template('proj1.html', shortURL=newURL)