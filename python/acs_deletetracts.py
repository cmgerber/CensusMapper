f = open('acsdata.csv','r')
t = open('acsdata2.csv','w')
for row in f.readlines():
    fips = row.split(',')[1]
    if len(fips) in [2,5] or fips[2:5] in ['001','013','041','055','075','081','085','087','095','097']:
        t.write(row)

f.close()
t.close()
exit()


