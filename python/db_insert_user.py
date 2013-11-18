#!../env/bin/python

from db_models import db, User
import flask
from flask import request
from hashlib import md5


@app.route('/create_account.html')
def create_account():
    #new user name input
    new_user_name = str(request.form['user_name'])
    new_email = str(request.form['new_email'])
    new_password = md5(str(request.form['new_password'])).hexdigest()
    new_user = User(new_user_name, new_email, new_password)

    #commits the new user to the db
    db.session.add(new_user)
    db.session.commit()