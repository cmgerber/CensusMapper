import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/Users/colingerber/Documents/Info 257/CensusMapper_Project/CensusMapperFlask/censusmapper.db'
db = SQLAlchemy(app)

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(80), unique=True)
    EmailAddress = db.Column(db.String(120), unique=True)
    Password = db.Column(db.Text)
    AccessLevel = db.Column(db.string(80))

    def __init__(self, username, email, Password):
        self.UserName = username
        self.EmailAddress = email
        self.Password = Password

    def __repr__(self):
        return '<User %r>' % self.username

class Map(db.Model):
    MapID = db.Column(db.Integer, primary_key=True)
    MapName = db.Column(db.String(200))
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    LatLongLowerLeft = db.Column(db.Float)
    LatLongUpperLeft = db.Column(db.Float)
    LatLongLowerRight = db.Column(db.Float)
    LatLongUpperRight = db.Column(db.Float)
    ZoomLevel = db.Column(db.Integer)

    def __init__(self, MapName, ZoomLevel, LatLongUpperRight, LatLongLowerRight, LatLongUpperLeft, LatLongLowerLeft):
        self.MapName = MapName
        self.LatLongUpperRight = LatLongUpperRight
        self.LatLongLowerRight = LatLongUpperRight
        self.LatLongUpperLeft = LatLongUpperLeft
        self.LatLongLowerLeft = LatLongLowerRight
        self.ZoomLevel = ZoomLevel

class DataLayers(db.Model):
    DataLayersID = db.Column(db.Integer, primary_key = True)
    MapID = db.Column(db.Integer, db.ForeignKey('Map.MapID'))
    MeasureID = db.Column(db.Integer, db.ForeignKey('Measure.MeasureID'))
    Year = db.Column(db.Integer)
    DisplayOrder = db.Column(db.Integer)
    DisplayGeography = db.Column(db.String(200))
    DisplayType = db.Column(db.String(200))
    Visible = db.Column(db.Boolean)
    ColorSchemeName = db.Column(db.String(200))
    NumCategories = db.Column(db.Integer)
    Transparency = db.Column(db.Float)

    def __init__(self, Year, DisplayOrder, DisplayGeography, DisplayType, Visible, ColorSchemeName, NumCategories, Transparency):
        self.Year = Year
        self.DisplayOrder = DisplayOrder
        self.DisplayGeography = DisplayGeography
        self.DisplayType = DisplayType
        self.Visible = Visible
        self.ColorSchemeName = ColorSchemeName
        self.NumCategories = NumCategories
        self.Transparency = Transparency

class ValueBreaks(db.Model):
    ValueBreaksID = db.Column(db.Integer, primary_key = True)
    DataLayersID = db.Column(db.Integer, ForeignKey('DataLayers.DataLayersID'))
    CatgoryNumber = db.Column(db.Integer)
    MaxValue = db.Column(db.Float)
    MinValue = db.Column(db.Float)

    def __init__(self, CatgoryNumber, MaxValue, MinValue):
        self.CatgoryNumber = CatgoryNumber
        self.MaxValue = MaxValue
        self.MinValue = MinValue

class ColorScheme(db.Model):
    ColorID = db.Column(db.Integer, primary_key = True)
    ColorSchemeName = db.Column(db.String(200))
    NumCategories = db.Column(db.Integer)
    CatgoryNumber = db.Column(db.Integer)
    RedValue = db.Column(db.Integer)
    GreenValue = db.Column(db.Integer)
    BlueValue = db.Column(db.Integer)

    def __init__(self, ColorSchemeName, NumCategories, CatgoryNumber, RedValue, GreenValue, BlueValue):
        self.ColorSchemeName = ColorSchemeName
        self.NumCategories = NumCategories
        self.CatgoryNumber = CatgoryNumber
        self.RedValue = RedValue
        self.GreenValue = GreenValue
        self.BlueValue = BlueValue

class Measures(db.Model):
    MeasureID = db.Column(db.Integer, primary_key = True)
    Description = db.Column(db.String(200))
    NumeratorID = db.Column(db.Integer)
    DenominatorID = db.Column(db.Integer)

    def __init__(self, Description, NumeratorID, DenominatorID):
        self.Description = Description
        self.NumeratorID = NumeratorID
        self.DenominatorID = DenominatorID

class Numerators(db.Model):
    NumeratorID = db.Column(db.Integer)
    FieldID = db.Column(db.Integer)

    def __init__(self, NumeratorID, FieldID):
        self.NumeratorID = NumeratorID
        self.FieldID = FieldID

class Denominators(db.Model):
    DenominatorID = db.Column(db.Integer)
    FieldID = db.Column(db.Integer)

    def __init__(self, DenominatorID, FieldID):
        self.DenominatorID = DenominatorID
        self.FieldID = FieldID
        