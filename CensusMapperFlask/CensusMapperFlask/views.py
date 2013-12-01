#!../env/bin/python

from CensusMapperFlask import app
from db_models import db, User, Map, DataLayer, ValueBreak, ColorScheme, Category, Measure, Numerator, Denominator, DefaultBreak
import flask
from flask import request
from hashlib import md5
from pgconn import API_KEY, secret_key
from uuid import uuid1


# homepage
@app.route('/')
def home():
    return flask.render_template('home.html')


# main mapping page
@app.route('/map')
def map():
    # get list of Census categories
    categories = [u.__dict__ for u in Category.query.all()]
    
    if 'userid' in flask.session:
        if 'mapid' in flask.session:
            mapobj = Map.query.filter_by(userid=flask.session['userid'], mapid=flask.session['mapid']).first()
            if mapobj:
                mapname = mapobj.mapname
                centerlat = mapobj.centerlatitude
                centerlong = mapobj.centerlongitude
                zoom = mapobj.zoomlevel
                return flask.render_template('main_map.html', mapname=mapname, centerlat=centerlat, centerlong=centerlong, zoom=zoom, categories=categories)
    else:
        new_user_name = 'temp_' + str(uuid1())
        new_user = User(new_user_name, '', '', 'regular')
        db.session.add(new_user)
        db.session.commit()
        flask.session['userid'] = new_user.userid

    mapname = 'Untitled Map'
    centerlat = 40
    centerlong = -98.5
    zoom = 4
    new_map = Map(mapname, flask.session['userid'], centerlat, centerlong, zoom)
    db.session.add(new_map)
    db.session.commit()
    flask.session['mapid'] = new_map.mapid
    return flask.render_template('main_map.html', mapname=mapname, centerlat=centerlat, centerlong=centerlong, zoom=zoom, categories=categories)


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
        #commits the new user to the db
        db.session.add(new_user)
        db.session.commit()
        flask.session['userid'] = new_user.userid
        flask.session['username'] = new_user.username
        remove_mapid()
    
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
        flask.session['userid'] = login_user.userid
        flask.session['username'] = login_user.username
        remove_mapid()
        flask.flash('You were successfully logged in')
        return flask.redirect(request.form['sourcepage'])
    
    # flask.flash('Your username or password did not mach. Please try again.')
    return flask.redirect(flask.url_for('home'))

# logout user request
@app.route('/logout')
def logout_of_account():
    #to log out of current session
    flask.session.pop('userid', None)
    flask.session.pop('username', None)
    remove_mapid()
    return flask.redirect(flask.url_for('home'))


# get available categories and measures
@app.route('/_get_measures')
def get_measures():
    # extract category id from element id
    categoryid = request.args['categoryid'].split('-')[1]
    measures = sorted([[m.measureid,m.description] for m in Measure.query.filter_by(categoryid=categoryid)], key=lambda x:x[0])
    return flask.jsonify(measures=measures)

# add layer for specific measure
@app.route('/_add_measure_layer')
def add_measure_layer():
    # get measure id
    measureid = request.args['measureid'].split('-')[1]
    measure = Measure.query.filter_by(measureid=measureid).first()
    
    #get numerator(s) and denominator(s)
    num = [n.fieldid for n in Numerator.query.filter_by(measureid=measureid)]
    nums = "'" + ("','").join(num) + "'"
    denom = [d.fieldid for d in Denominator.query.filter_by(measureid=measureid)]
    dens = "'" + ("','").join(denom) + "'"
    
    # get color scheme colors
    colorlist = list(db.engine.execute("select s.categorynumber, s.redvalue, s.greenvalue, s.bluevalue from measures m join categories c on m.categoryid=c.categoryid join colorschemes s on c.defaultcolorscheme=s.colorschemename and numcategories=5 where m.measureid = %s" % measureid))
    colors = {k: (r,g,b) for k, r, g, b in colorlist}
    
    # get five-category breaks
    breaks = list(DefaultBreak.query.filter_by(measureid=measureid, numcategories=5).order_by(DefaultBreak.categorynumber))
    bin_labels = [b.categorylabel for b in breaks]
    
    # generate css colors
    csscolors = ''
    for i in range(4,-1,-1):
        csscolors += '[measure <= %g] {polygon-fill: rgb(%d,%d,%d)} ' % (breaks[i].maxvalue,colors[i+1][0],colors[i+1][1],colors[i+1][2])

    cartocss = "#censusgeo { line-width: .1; line-color: #444444; polygon-opacity: 0; line-opacity: 0; " + \
               csscolors + "[zoom <= 4][geotype = 'state'] { polygon-opacity: 0.8; line-opacity: 1; } " + \
               "[zoom > 4][zoom <= 8][geotype = 'county'] { polygon-opacity: 0.72; line-opacity: 1; } " + \
               "[zoom > 4][zoom <= 8][geotype = 'state'] { polygon-opacity: 0; line-opacity: 1; line-width: 1; line-color: #444444; } " + \
               "[zoom > 8][geotype = 'tract'] { polygon-opacity: 0.64; line-opacity: 1; }}"
    sqlquery = "SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, " + \
               "sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end)" % nums
    if denom:
        sqlquery += " / (sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end) + 1)" % dens
    
    sqlquery += " measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode " + \
                "GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator"
    
    return flask.jsonify(sqlquery=sqlquery, cartocss=cartocss, bins=bin_labels, colors=colors, titletext=measure.description)


app.secret_key = secret_key

def remove_mapid():
    if 'mapid' in flask.session:
        flask.session.pop('mapid', None)

