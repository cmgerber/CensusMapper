#!../env/bin/python

from db_models import *
import flask
from flask import request
from hashlib import md5


#to access list of all the users in db
users = User.query.all()

@app.route('/login.html')
def login():
    #to access a user that logged in
    login_user_name = str(request.form['login_name'])
    login_user_password = md5(str(request.form['login_password']))hexdigest()
    login_user = User.query.filter_by(username='login_user_name').first()

    #check password
    login_user_password = #hash the password
    if login_user_password != login_user.password:
        raise Exception('Your username or password was incorrect, please try again.')