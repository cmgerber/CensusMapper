#!../env/bin/python 
# -*- coding: utf-8 -*-

from db_models import db, Numerator, Denominator
import csv,os,urllib
from state_lookup import state_lookup
from zipfile import ZipFile

# procedure to download file if it doesn't exist
def download(filename, url_path):
    """Downloads file into assets folder if it doesn't exist"""
    if not os.path.isfile('../assets/' + filename):
        print 'Could not find %s.  Downloading...' % filename
        retrieve = urllib.urlretrieve(url_path + filename, '../assets/' + filename)

# procedure to get element IDs from database
def get_elements():
    """Gets distinct numerator and denominator field IDs and returns as a list"""
    num = db.session.query(Numerator.fieldid).distinct()
    denom = db.session.query(Denominator.fieldid).distinct()
    return set([n[0] for n in num] + [d[0] for d in denom])

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
                table_loc[table_id]['elements'][row[3]] = row[7]
    
    return table_loc

# procedure to extract relevant geographic information
def extract_geo(csvfilename, sumlev):
    """Returns a dictionary of logrecno to FIPS codes for state, county, and tract"""
    
    output = {}
    
    geofile = open('../assets/' + csvfilename, 'r')
    geodata = csv.reader(geofile, quoting=csv.QUOTE_MINIMAL)
    
    for row in geodata:
        if row[2] == sumlev and row[3] == '00':
            logrecno = row[4]
            output[logrecno] = row[9]
            if sumlev in ['050','140']: output[logrecno] += row[10]
            if sumlev in ['140']: output[logrecno] += row[13]
    
    geofile.close()

    return output

# procedure to generate table data
def generate_table(element_list, geo, tab_lookup, filename):
    """Returns a list of lists representing "long skinny" version of table data
    
    Arguments:
        element_list - list of element IDs, all in the same table (eg ['B01001001',...])
        geo - geographic lookup dictionary of logrecno to FIPS code
        tab - table lookup dictionary for where to find table data
        filename - file name of zip archive, without the .zip extension (string)
    """
    
    output = []
    
    # get element start position
    table_id = element_list[0][:6]
    tab_info = tab_lookup[table_id]
    start = tab_info['start']
    
    year = filename[:4]
    
    # open data file
    acs_zip = ZipFile('../assets/' + filename + '.zip')
    datafile = acs_zip.open('e' + filename + '.txt')
    data = csv.reader(datafile, quoting=csv.QUOTE_MINIMAL)
    
    for row in data:
        logrecno = row[5]
        if logrecno in geo:
            fips = geo[logrecno]
            for e in element_list:
                output.append([e, fips, year, row[start + int(e[-3:]) - 2]])
    return output

# procedure to process requested tables for a given state (or national)
def process_geo(geography, level):
    """Returns a list of lists representing "long skinny" version of element data
    
    Arguments:
        geography - specific geography requested (eg 'California' or 'UnitedStates')
        level - geographic level (eg 'state', 'county', 'tract')
    """
    
    final = []
    
    # define folder locations on Census server
    url_base = 'http://www2.census.gov/acs2011_5yr/summaryfile/'
    data_folder = '2007-2011_ACSSF_By_State_By_Sequence_Table_Subset/'
    subfolder = {'tract': 'Tracts_Block_Groups_Only/',
                 'state': 'All_Geographies_Not_Tracts_Block_Groups/',
                 'county': 'All_Geographies_Not_Tracts_Block_Groups/'
                 }
    sumlev = {'tract': '140',
              'state': '040',
              'county': '050'
              }
    data_location = url_base + data_folder + geography + '/' + subfolder[level]
    
    # get list of desired elements from database
    elements = get_elements()
    
    # get unique list of tables
    tables = {}
    for e in elements:
        table_no = e[:6]
        if table_no not in tables: tables[table_no] = []
        tables[table_no].append(e)
    
    # create table lookup dictionary
    lookup_file = 'Sequence_Number_and_Table_Number_Lookup.txt'
    download(lookup_file, url_base)
    
    tab_lookup = table_lookup('../assets/' + lookup_file) # dictionary of table ID to info
    
    # get unique sequence files to grab
    seq = {}
    for t in tables:
        seq_no = tab_lookup[t]['seq']
        if seq_no not in seq: seq[seq_no] = []
        seq[seq_no].append(t)
    
    # generate geo lookups
    geofile = 'g20115' + state_lookup[geography] + '.csv'
    download(geofile, data_location)
    geo = extract_geo(geofile, sumlev[level]) # dictionary of logrecno to FIPS codes
    
    # extract the data table by table
    for s in sorted(seq):
        filename = '20115' + state_lookup[geography] + s + '000'
        download(filename + '.zip', data_location)
        for t in seq[s]:
            final += generate_table(sorted(tables[t]), geo, tab_lookup, filename)
    
    return final

if __name__ == '__main__':
    
    # clear existing file, if any
    outfile = 'acsdata.tab'
    if os.path.isfile('../assets/' + outfile): os.remove('../assets/' + outfile)
    
    f = open('../assets/' + outfile,'a')
    
    for state in sorted(state_lookup.keys()):
        print state
        final = process_geo(state, 'state')
        final += process_geo(state, 'county')
        for row in final:
            f.write(','.join(row) + '\n')
    
    final = process_geo('California', 'tract')
    for row in final:
        f.write(','.join(row) + '\n')
    
    f.close()

