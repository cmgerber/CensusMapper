#!../env/bin/python

from CensusMapperFlask import app
from db_models import db, User
import flask
from flask import request
from hashlib import md5


@app.route('/login', methods = ['POST'])
def login_to_account():
    #to access a user that logged in
    login_user_name = str(request.form['login_name'])
    login_user_password = md5(str(request.form['login_password'])).hexdigest()
    login_user = User.query.filter_by(username=login_user_name).first()

    #check password
    if login_user_password != login_user.password:
        raise Exception('Your username or password was incorrect, please try again.')

    return flask.render_template('logged_in.html', username = login_user_name)

#how the tutorial shows doing logout
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))