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
    if 'userid' in flask.session:
        if 'mapid' in flask.session:
            mapobj = Map.query.filter_by(userid=flask.session['userid'], mapid=flask.session['mapid']).first()
            if mapobj:
                mapname = mapobj.mapname
                centerlat = mapobj.centerlatitude
                centerlong = mapobj.centerlongitude
                zoom = mapobj.zoomlevel
                return flask.render_template('main_map.html', mapname=mapname, centerlat=centerlat, centerlong=centerlong, zoom=zoom, categories=category_list())
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
    flask.session['displayorder'] = 0
    
    return flask.render_template('main_map.html', mapname=mapname, centerlat=centerlat, centerlong=centerlong, zoom=zoom, categories=category_list())


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
    measures = []
    measure_list = Measure.query.filter_by(categoryid=categoryid).order_by(Measure.measureid)
    for m in measure_list:
        denom = True if [d.fieldid for d in Denominator.query.filter_by(measureid=m.measureid)] else False
        measures.append([m.measureid, m.description, denom])
    return flask.jsonify(measures=measures)

# add layer for specific measure
@app.route('/_add_measure_layer')
def add_measure_layer():
    # get measure id
    measureid = request.args['measureid'].split('-')[1]
    measure = Measure.query.filter_by(measureid=measureid).first()
    
    # get category
    category = Category.query.filter_by(categoryid=measure.categoryid).first()
    
    # add datalayer to map
    year = 2011
    flask.session['displayorder'] += 1
    displaygeography = 'default'
    displaytype = 'solid choropleth'
    visible = True
    colorschemename = category.defaultcolorscheme
    numcategories = 5
    transparency = 0.8
    
    new_layer = DataLayer(flask.session['mapid'], measureid, year, flask.session['displayorder'], displaygeography, displaytype, visible, colorschemename, numcategories, transparency)
    db.session.add(new_layer)
    db.session.commit()
    new_layer_id = new_layer.datalayersid
    
    # add value breaks
    breaks = [b.maxvalue for b in DefaultBreak.query.filter_by(measureid=measureid, numcategories=numcategories).order_by(DefaultBreak.categorynumber)]
    for b in range(len(breaks)):
        new_value_break = ValueBreak(new_layer_id, b+1, 0 if b == 0 else breaks[b-1], breaks[b])
        db.session.add(new_value_break)
        db.session.commit()
    
    return flask.jsonify(layerid=new_layer_id)


@app.route('/_render_layer')
def render_layer():
    # get layer id
    layerid = int(request.args['layerid'])
    return generate_layer(layerid)


@app.route('/_set_census_viz')
def set_census_viz():
    # get layer id
    layerid = int(request.args['layerid'])
    flask.session['censusviz'] = layerid
    return flask.jsonify(layerid=layerid)


@app.route('/_remove_layer')
def remove_layer():
    # get measure id
    measureid = request.args['measureid'].split('-')[1]
    
    # get user id
    mapid = flask.session['mapid']
    
    # get datalayersid
    layerid = DataLayer.query.filter_by(mapid=mapid, measureid=measureid).first().datalayersid
    
    # remove from datalayers
    remove_sql = "delete from datalayers where datalayersid = %d" % (layerid)
    db.engine.execute(remove_sql)
    db.session.commit()
    
    # reorder the layers (to do)
    
    # if necessary, get next datalayerid for display
    if flask.session['censusviz'] == layerid:
        nextlayer = DataLayer.query.filter_by(mapid=mapid).order_by(DataLayer.displayorder).first()
        if nextlayer:
            return flask.jsonify(layerid=layerid, nextid=nextlayer.datalayersid)
        else:
            return flask.jsonify(layerid=layerid, remove_all=True)
    
    return flask.jsonify(layerid=layerid)


app.secret_key = secret_key

# some helper functions...

def remove_mapid():
    if 'mapid' in flask.session:
        flask.session.pop('mapid', None)

def category_list():
    return [u.__dict__ for u in Category.query.all()]

def generate_layer(layerid):
    layerinfo = DataLayer.query.filter_by(datalayersid=layerid).first()
    measureid = layerinfo.measureid
    
    # get measure description text
    measure = Measure.query.filter_by(measureid=measureid).first()
    titletext = measure.description
    
    # get colors and breaks
    color_sql = "select c.categorynumber, v.maxvalue, c.redvalue, c.greenvalue, c.bluevalue " + \
                "from datalayers d join colorschemes c on d.colorschemename = c.colorschemename and d.numcategories = c.numcategories " + \
                "  join valuebreaks v ON d.datalayersid = v.datalayersid and v.categorynumber = c.categorynumber " + \
                "where d.datalayersid = %d" % layerid
    colorlist = list(db.engine.execute(color_sql))
    colors = {k: (m,(r,g,b)) for k, m, r, g, b in colorlist}
    
    # write cartocss
    cartocss = "#censusgeo { line-width: .1; line-color: #444444; polygon-opacity: 0; line-opacity: 0; "
    for c in sorted(colors.keys(), reverse=True):
        cartocss += '[measure <= %g] {polygon-fill: rgb(%d,%d,%d)} ' % (colors[c][0],colors[c][1][0],colors[c][1][1],colors[c][1][2])
    
    if layerinfo.displaygeography == 'default':
        cartocss += "[zoom <= 4][geotype = 'state'] { polygon-opacity: %g; line-opacity: 1; } " % (layerinfo.transparency) + \
                    "[zoom > 4][zoom <= 8][geotype = 'county'] { polygon-opacity: %g; line-opacity: 1; } " % (layerinfo.transparency * 0.9) + \
                    "[zoom > 4][zoom <= 8][geotype = 'state'] { polygon-opacity: 0; line-opacity: 1; line-width: 1; line-color: #444444; } " + \
                    "[zoom > 8][geotype = 'tract'] { polygon-opacity: %g; line-opacity: 1; }" % (layerinfo.transparency * 0.8)
    else:
        cartocss += "[geotype = '%s'] { polygon-opacity: %g; line-opacity: 1; }" % (layerinfo.displaygeography, layerinfo.transparency)
    
    cartocss += "}"
    
    #get numerator(s) and denominator(s)
    num = [n.fieldid for n in Numerator.query.filter_by(measureid=measureid)]
    nums = "'" + ("','").join(num) + "'"
    denom = [d.fieldid for d in Denominator.query.filter_by(measureid=measureid)]
    dens = "'" + ("','").join(denom) + "'"
    
    # write sql query
    sqlquery = "SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, " + \
               "sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end)" % nums
    if denom:
        sqlquery += " / (sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end) + 1)" % dens
    
    sqlquery += " measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode " + \
                "GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator"
    
    # generate bin labels
    bins = [b.maxvalue for b in ValueBreak.query.filter_by(datalayersid=layerid).order_by(ValueBreak.categorynumber)]
    avg_bin = sum(bins[:-1]) / len(bins[:-1])
    bin_labels = []
    
    for c in range(layerinfo.numcategories):
        if avg_bin < 0.1:
            bin_labels.append('%.1f%% to %.1f%%' % (100.0 * 0 if c == 0 else 100.0 * bins[c-1], 100.0 * bins[c]))
        elif avg_bin < 1:
            bin_labels.append('%.0f%% to %.0f%%' % (100.0 * 0 if c == 0 else 100.0 * bins[c-1], 100.0 * bins[c]))
        else:
            bin_labels.append('{0:,}'.format(0 if c == 0 else int(bins[c-1])) + ' to ' + '{0:,}'.format(int(bins[c])))
    
    return flask.jsonify(sqlquery=sqlquery, cartocss=cartocss, bins=bin_labels, colors=colors, titletext=titletext, layerid=layerid)

