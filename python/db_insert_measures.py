#!../env/bin/python

from db_models import db, Measure, Numerator, Denominator

# define columns
columns = ['Category', 'Numerator', 'Denominator', 'Description', 'Universe']

# open file
f = open('../assets/acs_measures.csv','r')

# generate inserts for each line
for r in f.readlines():
    
    datadict = dict(zip(columns,r.strip().split(',')))
    print ('%s: %s' % (datadict['Category'], datadict['Description']))
    
    # insert measure description info
    measure = Measure(datadict['Category'], datadict['Description'])
    db.session.add(measure)
    db.session.commit()
    measureid = measure.measureid
    
    # insert numerator and denominator fields
    num = datadict['Numerator'].split('+')
    denom = datadict['Denominator'].split('+')
    
    for n in num:
        ins = Numerator(measureid,n)
        db.session.add(ins)
    
    for d in denom:
        if d:
            ins = Denominator(measureid,d)
            db.session.add(ins)
    
    db.session.commit()

# close file
f.close()

