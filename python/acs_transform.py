#! env/bin/python 
# -*- coding: utf-8 -*-

from zipfile import ZipFile
import os,csv,urllib

# procedure to generate table lookup dictionary
def table_lookup(filename):
    """Returns a dictionary providing file and field information for each table"""
    
    table_loc = {}
    
    f = open(filename,'r')
    data = csv.reader(f)
    
    for row in data:
        if row[0] == 'ACSSF':
            table_id = row[1]
            if table_id not in table_loc:
                table_loc[table_id] = {'seq': row[2],
                                       'start': int(row[4]),
                                       'title': row[7],
                                       'elements': {}}
            elif row[7][:8] == 'Universe':
                table_loc[table_id]['universe'] = row[7][10:]
            elif '.' not in row[3]:
                table_loc[table_id]['elements'][int(row[3])] = row[7]
    
    return table_loc

# procedure to extract relevant geographic information
def extract_geo(zipfilename):
    """Returns a dictionary of logrecno to FIPS codes for state, county, and tract"""
    
    output = {}
    
    acs_zip = ZipFile(zipfilename)
    filename = [f for f in acs_zip.namelist() if f[0] == 'g' and f[-3:] == 'csv'][0]
    geofile = acs_zip.open(filename)
    geodata = csv.reader(geofile, quoting=csv.QUOTE_MINIMAL)
    
    for row in geodata:
        sumlev = row[2]
        logrecno = row[4]
        if row[3] != '00': sumlev = ''
        
        if sumlev in ['040','050','140']: output[logrecno] = row[9]
        if sumlev in ['050','140']: output[logrecno] += row[10]
        if sumlev in ['140']: output[logrecno] += row[13]
    
    return output

# procedure to generate table data
def generate_table(tab_id, geo, tab_lookup, zipfilename):
    """Returns a list of lists representing "long skinny" version of table data
    
    Arguments:
        tab_id - ID of table (eg 'B01001')
        geo - geographic lookup dictionary of logrecno to FIPS code
        tab - table lookup dictionary for where to find table data
        zipfilename - file name of zip archive (string)
    """
    
    output = []
    
    tab_info = tab_lookup[tab_id]
    acs_zip = ZipFile(zipfilename)
    filename = [f for f in acs_zip.namelist() if f[0] == 'e' and f[-11:] == tab_info['seq'].zfill(4) + '000.txt'][0]
    datafile = acs_zip.open(filename)
    data = csv.reader(datafile, quoting=csv.QUOTE_MINIMAL)
    
    year = filename[1:5]
    start = tab_info['start']
    
    for row in data:
        logrecno = row[5]
        if logrecno in geo:
            fips = geo[logrecno]
            for pos, val in sorted(tab_info['elements'].items(), key=lambda x: x[0]):
                output.append([tab_id + str(pos).zfill(3), fips, year, row[start + pos - 2]])
    
    return output

# procedure to process requested tables for a given state
def process_state(state, tables):
    """Returns a list of lists representing "long skinny" version of table data
    
    Arguments:
        state - state name (string, eg 'California')
        tables - list of table ID strings (eg ['B01001'])
    """
    
    url_base = 'http://www2.census.gov/acs2011_5yr/summaryfile/'
    data_folder = '2007-2011_ACSSF_By_State_All_Tables/'
    file_ext = ['_All_Geographies_Not_Tracts_Block_Groups.zip','_Tracts_Block_Groups_Only.zip']
    for f in file_ext:
        if not os.path.isfile(state + f):
            print "Could not find %s%s. Downloading..." % (state, f)
            urllib.urlretrieve(url_base + data_folder + state + f, state + f)
    
    lookup_file = 'Sequence_Number_and_Table_Number_Lookup.txt'
    if not os.path.isfile(lookup_file):
        urllib.urlretriev(url_base + lookup_file, lookup_file)
    
    tab_lookup = table_lookup(lookup_file)
    final = []
    for f in file_ext:
        geo = extract_geo(state + f)
        for t in tables:
            final += generate_table(t, geo, tab_lookup, state + f)
    
    return final

if __name__ == '__main__':
    
    # clear existing file, if any
    outfile = 'acsdata.tab'
    if os.path.isfile(outfile): os.remove(outfile)
    
    final = process_state('California', ['B03002'])
    
    # write output
    f = open(outfile,'a')
    for row in final:
        f.write('\t'.join(row) + '\n')
    f.close()

