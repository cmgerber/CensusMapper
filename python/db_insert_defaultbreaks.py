#!../env/bin/python

from cartodb import CartoDBAPIKey, CartoDBException
from db_models import db, Measure, Numerator, Denominator, DefaultBreak
from pgconn import API_KEY, secret_key

# establish connection to CartoDB server
def connect_to_cartodb():
    return CartoDBAPIKey(API_KEY, 'censusmapper')

cl = connect_to_cartodb()

# loop through measures to generate values for 3- through 9-category breaks
measures = Measure.query.all()
for m in measures:
    
    print m.description
    
    #get numerator(s) and denominator(s)
    num = [n.fieldid for n in Numerator.query.filter_by(measureid=m.measureid)]
    nums = "'" + ("','").join(num) + "'"
    denom = [d.fieldid for d in Denominator.query.filter_by(measureid=m.measureid)]
    dens = "'" + ("','").join(denom) + "'"
    
    #get highest value
    sql_query = "select max(measure) maxval " + \
                "from (SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, " + \
                "sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end)" % nums
    if denom:
        sql_query += " / (sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end) + 1)" % dens
    sql_query += " measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode " + \
                "GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator) layer"
    
    s = cl.sql(sql_query)
    maxval = s['rows'][0]['maxval']
    
    # write jenks sql with "ZZZZZ" in place of number of breaks
    sql_temp = "select CDB_JenksBins(array_agg(measure::numeric), ZZZZZ) cdb_jenksbins " + \
               "from (SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, " + \
               "sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end)" % nums
    if denom:
        sql_temp += " / (sum(case when b.fieldid in (%s) then cast(b.value as float) else 0 end) + 1)" % dens
    sql_temp += " measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode where length(a.fipscode) = 5 " + \
               "GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator) layer"
    
    # loop through different categories and write values to database
    for numcat in range(3,10):
        print numcat
        sql_query = sql_temp.replace('ZZZZZ',str(numcat))
        s = cl.sql(sql_query)
        bins = s['rows'][0]['cdb_jenksbins']
        avg_bin = sum(bins) / len(bins)
            
        for c in range(numcat):
            if avg_bin < 0.1:
                label = '%.1f%% to %.1f%%' % (100.0 * 0 if c == 0 else 100.0 * bins[c-1], 100.0 * maxval if c == numcat - 1 else 100.0 * bins[c])
            elif avg_bin < 1:
                label = '%.0f%% to %.0f%%' % (100.0 * 0 if c == 0 else 100.0 * bins[c-1], 100.0 * maxval if c == numcat - 1 else 100.0 * bins[c])
            else:
                label = '{0:,}'.format(0 if c == 0 else int(bins[c-1])) + ' to ' + '{0:,}'.format(maxval if c == numcat - 1 else int(bins[c]))
            
            defbreak = DefaultBreak(m.measureid, numcat, c+1, maxval if c == numcat - 1 else bins[c], label)
            db.session.add(defbreak)
            db.session.commit()


