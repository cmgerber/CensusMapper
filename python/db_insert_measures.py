#!../env/bin/python

from db_models import db, Category, Measure, Numerator, Denominator

# define columns
columns = ['Category', 'Numerator', 'Denominator', 'Description', 'Universe']

# define default color schemes
colorscheme = {'Age': 'Reds',
               'Education': 'Blues',
               'Employment': 'Purples',
               'Housing': 'RdPu',
               'Income': 'Greens',
               'Population': 'Oranges',
               'Race': 'YlOrBr',
               'Sex': 'BuGn'}

# open file
f = open('../assets/acs_measures.csv','r')

# generate inserts for each line
for r in f.readlines():
    
    datadict = dict(zip(columns,r.strip().split(',')))
    cat = datadict['Category']
    desc = datadict['Description']
    print ('%s: %s' % (cat, datadict['Description']))
    
    # insert category info if necessary
    category = Category.query.filter_by(category=cat).first()
    if not category:
        category = Category(cat, colorscheme[cat], None)
        db.session.add(category)
        db.session.commit()
    
    categoryid = category.categoryid
    
    # insert measure description info
    measure = Measure(categoryid, datadict['Description'])
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

