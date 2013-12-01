import flask
from flask.ext.sqlalchemy import SQLAlchemy
from pgconn import pgconn

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = pgconn
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    emailaddress = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    accesslevel = db.Column(db.String(10))
    
    def __init__(self, username, email, password, accesslevel):
        self.username = username
        self.emailaddress = email
        self.password = password
        self.accesslevel = accesslevel


class Map(db.Model):
    __tablename__ = 'maps'
    
    mapid = db.Column(db.Integer, primary_key=True)
    mapname = db.Column(db.String(50))
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    centerlatitude = db.Column(db.Float)
    centerlongitude = db.Column(db.Float)
    zoomlevel = db.Column(db.Integer)
    
    def __init__(self, mapname, userid, centerlatitude, centerlongitude, zoomlevel):
        self.mapname = mapname
        self.userid = userid
        self.centerlatitude = centerlatitude
        self.centerlongitude = centerlongitude
        self.zoomlevel = zoomlevel

class DataLayer(db.Model):
    __tablename__ = 'datalayers'
    
    datalayersid = db.Column(db.Integer, primary_key = True)
    mapid = db.Column(db.Integer, db.ForeignKey('maps.mapid'))
    measureid = db.Column(db.Integer, db.ForeignKey('measures.measureid'))
    year = db.Column(db.Integer)
    displayorder = db.Column(db.Integer)
    displaygeography = db.Column(db.String(20))
    displaytype = db.Column(db.String(20))
    visible = db.Column(db.Boolean)
    colorschemename = db.Column(db.String(8))
    numcategories = db.Column(db.Integer)
    transparency = db.Column(db.Float)
    
    def __init__(self, mapid, measureid, year, displayorder, displaygeography, displaytype, visible, colorschemename, numcategories, transparency):
        self.mapid = mapid
        self.measureid = measureid
        self.year = year
        self.displayorder = displayorder
        self.displaygeography = displaygeography
        self.displaytype = displaytype
        self.visible = visible
        self.colorschemename = colorschemename
        self.numcategories = numcategories
        self.transparency = transparency

class ValueBreak(db.Model):
    __tablename__ = 'valuebreaks'
    
    valuebreaksid = db.Column(db.Integer, primary_key = True)
    datalayersid = db.Column(db.Integer, db.ForeignKey('datalayers.datalayersid'))
    categorynumber = db.Column(db.Integer)
    maxvalue = db.Column(db.Float)
    minvalue = db.Column(db.Float)
    
    def __init__(self, datalayersid, categorynumber, minvalue, maxvalue):
        self.datalayersid = datalayersid
        self.categorynumber = categorynumber
        self.minvalue = minvalue
        self.maxvalue = maxvalue

class ColorScheme(db.Model):
    __tablename__ = 'colorschemes'
    
    colorid = db.Column(db.Integer, primary_key = True)
    colorschemename = db.Column(db.String(8))
    numcategories = db.Column(db.Integer)
    criticalvalue = db.Column(db.Float)
    categorynumber = db.Column(db.Integer)
    redvalue = db.Column(db.Integer)
    greenvalue = db.Column(db.Integer)
    bluevalue = db.Column(db.Integer)
    schemetype = db.Column(db.String(11))
    
    def __init__(self, colorschemename, numcategories, criticalvalue, categorynumber, redvalue, greenvalue, bluevalue, schemetype):
        self.colorschemename = colorschemename
        self.numcategories = numcategories
        self.criticalvalue = criticalvalue
        self.categorynumber = categorynumber
        self.redvalue = redvalue
        self.greenvalue = greenvalue
        self.bluevalue = bluevalue
        self.schemetype = schemetype

class Category(db.Model):
    __tablename__ = 'categories'
    
    categoryid = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(20))
    defaultcolorscheme = db.Column(db.String(8))
    
    def __init__(self, category, defaultcolorscheme):
        self.category = category
        self.defaultcolorscheme = defaultcolorscheme

class Measure(db.Model):
    __tablename__ = 'measures'
    
    measureid = db.Column(db.Integer, primary_key = True)
    categoryid = db.Column(db.Integer, db.ForeignKey('categories.categoryid'))
    description = db.Column(db.String(100))
    
    def __init__(self, categoryid, description):
        self.categoryid = categoryid
        self.description = description

class Numerator(db.Model):
    __tablename__ = 'numerator'
    
    numeratorid = db.Column(db.Integer, primary_key = True)
    measureid = db.Column(db.Integer, db.ForeignKey('measures.measureid'))
    fieldid = db.Column(db.Integer)
    
    def __init__(self, measureid, fieldid):
        self.measureid = measureid
        self.fieldid = fieldid

class Denominator(db.Model):
    __tablename__ = 'denominator'
    
    denominatorid = db.Column(db.Integer, primary_key = True)
    measureid = db.Column(db.Integer, db.ForeignKey('measures.measureid'))
    fieldid = db.Column(db.Integer)
    
    def __init__(self, measureid, fieldid):
        self.measureid = measureid
        self.fieldid = fieldid

class DefaultBreak(db.Model):
    __tablename__ = 'defaultbreaks'
    
    defaultbreakid = db.Column(db.Integer, primary_key = True)
    measureid = db.Column(db.Integer, db.ForeignKey('measures.measureid'))
    numcategories = db.Column(db.Integer)
    categorynumber = db.Column(db.Integer)
    maxvalue = db.Column(db.Float)
    categorylabel = db.Column(db.String(30))
    
    def __init__(self, measureid, numcategories, categorynumber, maxvalue, categorylabel):
        self.measureid = measureid
        self.numcategories = numcategories
        self.categorynumber = categorynumber
        self.maxvalue = maxvalue
        self.categorylabel = categorylabel

