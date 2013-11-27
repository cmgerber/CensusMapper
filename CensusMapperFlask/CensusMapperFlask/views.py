#!../env/bin/python

from CensusMapperFlask import app
from db_models import db, User, Category, Measure, Numerator, Denominator
import flask
from flask import request
from hashlib import md5
from pgconn import secret_key

# homepage
@app.route('/')
def home():
    return flask.render_template('home.html')


# main mapping page
@app.route('/map')
def map():
    # get list of categories
    categories = [u.__dict__ for u in Category.query.all()]
    return flask.render_template('main_map.html', mapname='Untitled Map', categories=categories)


# create user request
@app.route('/create_user', methods = ['POST'])
def create_account():
    #new user name input
    new_user_name = str(request.form['new_name'])
    new_email = str(request.form['new_email'])
    new_password1 = md5(str(request.form['new_password1'])).hexdigest()
    new_password2 = md5(str(request.form['new_password2'])).hexdigest()
    new_access = 'regular'
    new_user = User(new_user_name, new_email, new_password1, new_access)
    
    if new_password1 == new_password2:
        flask.session['username'] = new_user_name
        #commits the new user to the db
        db.session.add(new_user)
        db.session.commit()
    
    #flask.flash('New account was successfully created. Please login.')
    return flask.redirect(flask.url_for('home'))

# login user request
@app.route('/login', methods = ['POST'])
def login_to_account():
    #to access a user that logged in
    login_user_name = str(request.form['login_name'])
    login_user_password = md5(str(request.form['login_password'])).hexdigest()
    login_user = User.query.filter_by(username=login_user_name, password=login_user_password).first()
    
    #check password
    if login_user:
        flask.session['username'] = login_user_name
        flask.flash('You were successfully logged in')
        return flask.redirect(request.form['sourcepage'])
    
    # flask.flash('Your username or password did not mach. Please try again.')
    return flask.redirect(flask.url_for('home'))

# logout user request
@app.route('/logout')
def logout_of_account():
    #to log out of current session
    flask.session.pop('username', None)
    return flask.redirect(flask.url_for('home'))


# get available categories and measures
@app.route('/_get_measures')
def get_measures():
    # extract category id from element id
    categoryid = request.args['categoryid'].split('-')[1]
    
    return

# add layer request
@app.route('/_add_layer')
def add_layer():
    
    cartocss = "#censusgeo { line-width: .1; line-color: #444444; polygon-opacity: 0; line-opacity: 0;[ measure <= 1.00 ] { polygon-fill: rgb(179,0,0)}[ measure <= 0.40 ] { polygon-fill: rgb(227,51,74)}[ measure <= 0.25 ] { polygon-fill: rgb(252,89,141)}[ measure <= 0.15 ] { polygon-fill: rgb(253,138,204)}[ measure <= 0.05 ] { polygon-fill: rgb(254,217,240)} [zoom <= 4][geotype = 'state'] { polygon-opacity: 0.8; line-opacity: 1; } [zoom > 4][zoom <= 8][geotype = 'county'] { polygon-opacity: 0.72; line-opacity: 1; } [zoom > 4][zoom <= 8][geotype = 'state'] { polygon-opacity: 0; line-opacity: 1; line-width: 1; line-color: #222222; } [zoom > 8][geotype = 'tract'] { polygon-opacity: 0.64; line-opacity: 1; }}"
    sqlquery = "SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, sum(case when b.fieldid in ('B03002012') then cast(b.value as float) else 0 end)/(sum(case when b.fieldid in ('B01001001') then cast(b.value as float) else 0 end) + 1) measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator"
    
    js_command = ''

    print 'here'
    
    return flask.jsonify(sqlquery=sqlquery, cartocss=cartocss, js_command=js_command)

app.secret_key = secret_key