#!../env/bin/python

from db_models import db, User, Map, DataLayer, ValueBreak, Measure
from hashlib import md5

def commit(row):
    """commits the row to the database db"""
    db.session.add(row)
    db.session.commit()

u = User('sandra', 'sandra@ischool.berkeley.edu', 'sandra', 'regular')
commit(u)
m = Map('Median income', u.userid, 38, -120, 6)
commit(m)
measure = Measure.query.filter_by(description='Median Income in the Past 12 Months').first()
d = DataLayer(m.mapid, measure.measureid, 2011, 1, 'default', 'solid choropleth', True, 'BuGn', 5, 0.9)
commit(d)
d = DataLayer.query.filter_by(datalayersid=1).first()
breaks = [25000, 50000, 75000, 100000, 100000000]
for i, b in enumerate(breaks):
    v = ValueBreak(d.datalayersid, i + 1, breaks[i-1] if i > 0 else 0, b)
    commit(v)

u = User('colin', 'colin.gerber@ischool.berkeley.edu', 'colin', 'regular')
commit(u)


u = User('jason', 'jost@ischool.berkeley.edu', 'jason', 'regular')
commit(u)

