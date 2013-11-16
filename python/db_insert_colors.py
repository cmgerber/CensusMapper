#!../env/bin/python

from db_models import db, ColorScheme

# define columns
columns = ['ColorSchemeName', 'NumCategories', 'CriticalValue' ,'CategoryNumber', 'RedValue', 'GreenValue', 'BlueValue', 'SchemeType']

# open file
f = open('../assets/colorbrewer.csv','r')

# generate inserts for each line
for r in f.readlines():
    
    datadict = dict(zip(columns,r.strip().split(',')))
    
    # insert color info
    color = ColorScheme(datadict['ColorSchemeName'],
                        int(datadict['NumCategories']) if datadict['NumCategories'] else None,
                        float(datadict['CriticalValue']) if datadict['CriticalValue'] else None,
                        int(datadict['CategoryNumber']) if datadict['CategoryNumber'] else None,
                        int(datadict['RedValue']) if datadict['RedValue'] else None,
                        int(datadict['GreenValue']) if datadict['GreenValue'] else None,
                        int(datadict['BlueValue']) if datadict['BlueValue'] else None,
                        datadict['SchemeType'])
    db.session.add(color)

db.session.commit()

# close file
f.close()

