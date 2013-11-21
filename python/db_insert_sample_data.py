#!../env/bin/python

from db_models import db, User, Map, DataLayer, ValueBreak, Measure
from hashlib import md5

def commit(row):
    """commits the row to the database db"""
    db.session.add(row)
    db.session.commit()

u = User('sandra', 'sandra@ischool.berkeley.edu', 'sandra', 'regular')
commit(u)
# mapname, userid, centerlatitude, centerlongitude, zoomlevel
m = Map('Median income', u.userid, 38, -120, 6)
commit(m)
measure = Measure.query.filter_by(description='Median Income in the Past 12 Months').first()
# mapid, measureid, year, displayorder, displaygeography, displaytype, visible, colorschemename, numcategories, transparency
d = DataLayer(m.mapid, measure.measureid, 2011, 1, 'default', 'solid choropleth', True, 'BuGn', 5, 0.9)
commit(d)
# max of each break category
breaks = [25000, 50000, 75000, 100000, 100000000]
for i, b in enumerate(breaks):
    # datalayersid, categorynumber, minvalue, maxvalue
    v = ValueBreak(d.datalayersid, i + 1, breaks[i-1] if i > 0 else 0, b)
    commit(v)

u = User('colin', 'colin.gerber@ischool.berkeley.edu', 'colin', 'regular')
commit(u)
m = Map('Hispanic', u.userid, 40, -98.5, 4)
commit(m)
measure = Measure.query.filter_by(description='Percent Hispanic or Latino').first()
d = DataLayer(m.mapid, measure.measureid, 2011, 1, 'default', 'solid choropleth', True, 'OrRd', 5, 0.9)
commit(d)
breaks = [0.05, 0.15, 0.25, 0.40, 1]
for i, b in enumerate(breaks):
    v = ValueBreak(d.datalayersid, i + 1, breaks[i-1] if i > 0 else 0, b)
    commit(v)

m = Map('Black', u.userid, 40, -98.5, 4)
commit(m)
measure = Measure.query.filter_by(description='Percent Black or African American alone').first()
d = DataLayer(m.mapid, measure.measureid, 2011, 1, 'default', 'solid choropleth', True, 'PuBu', 5, 0.9)
commit(d)
breaks = [0.05, 0.10, 0.20, 0.35, 1]
for i, b in enumerate(breaks):
    v = ValueBreak(d.datalayersid, i + 1, breaks[i-1] if i > 0 else 0, b)
    commit(v)



u = User('jason', 'jost@ischool.berkeley.edu', 'jason', 'regular')
commit(u)
m = Map('Unemployment', u.userid, 38, -120, 7)
commit(m)
measure = Measure.query.filter_by(description='Percent Unemployed').first()
d = DataLayer(m.mapid, measure.measureid, 2011, 1, 'default', 'solid choropleth', True, 'PuRd', 5, 0.9)
commit(d)
breaks = [0.05, 0.07, 0.09, 0.11, 1]
for i, b in enumerate(breaks):
    v = ValueBreak(d.datalayersid, i + 1, breaks[i-1] if i > 0 else 0, b)
    commit(v)


