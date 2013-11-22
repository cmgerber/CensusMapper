#!../env/bin/python

from CensusMapperFlask import app
from db_models import db, User
import flask
from flask import request, flash
from hashlib import md5


@app.route('/create_user', methods = ['POST'])
def create_account():
    #new user name input
    new_user_name = str(request.form['new_name'])
    new_email = str(request.form['new_email'])
    new_password = md5(str(request.form['new_password'])).hexdigest()
    new_access = 'regular'
    new_user = User(new_user_name, new_email, new_password, new_access)

    #commits the new user to the db
    db.session.add(new_user)
    db.session.commit()

    #flash('New account was successfully created. Please login.')
    return flask.render_template('logged_in.html', username = new_user_name)