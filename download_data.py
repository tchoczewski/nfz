# =============================================================================
# Script to download data from NFZ Statistics API:
# https://api.nfz.gov.pl/app-stat-api-jgp/
# =============================================================================

import requests
import pandas as pd
import time
import urllib.parse
import os
import sys

TIME_API = 0.1 # Maximal HTTP requests per second is 10 due to NFZ Statistics API rules
MAX_ATTEMPTS = 5 # Maximal requests attempts for one URL
year_list = list(range(2009, 2019)) # Years from 2009-2018 for which data will be downloaded

# =============================================================================
# Functions
# =============================================================================

def get_html(path, delta): # Get JSON requests
    if delta <= TIME_API:
        time.sleep(TIME_API - delta)
    attempts = 0
    while (attempts < MAX_ATTEMPTS):
        try:
            with requests.Session() as ses:
                json_file = ses.get(path).json()
            break
        except requests.exceptions.RequestException:
            attempts += 1
            print("attempts: " + str(attempts))
    if (attempts == MAX_ATTEMPTS):
        print("Data download failed, check your internet connection")
        sys.exit()
    return json_file

def benefits(): # Download the benefits dictionary (catalogs: 1a - Jednorodne Grupy Pacjentow, 1b - Katalog swiadczen odrebnych, 1c - Katalog swiadczen do sumowania, 1d - Katalog swiadczen radioterapii, 1w - Katalog swiadczen wysokospecjalistycznych)
    filepath = 'data/benefits.csv'
    if os.path.isfile(filepath):
        return
    start_time = time.time()
    time1 = start_time
    catalogs = ['1a', '1b', '1c', '1d', '1w']
    benefits = pd.DataFrame(columns = ['code', 'name', 'catalog'])
    for catalog in catalogs:
        page = 0
        not_empty = True
        while (not_empty):
            page += 1
            path = 'https://api.nfz.gov.pl/app-stat-api-jgp/benefits?benefit=%%%&catalog=' + catalog + '&format=json&limit=25&api-version=1.0' + '&page=' + str(page)
            delta = time.time() - time1
            json_file = get_html(path, delta)
            time1 = time.time()
            df = pd.json_normalize(json_file["data"])
            df['catalog'] = catalog
            benefits = benefits.append(df)
            not_empty = (len(df) > 0)
    benefits = benefits.drop_duplicates()
    benefits.to_csv(filepath, index = False)  
    print("Runtime - benefits: " + str(round(time.time() - start_time, 2)))
    
def index_of_tables(year): # Download the list of all available tables
    filepath = 'data/annual/index-of-tables-' + str(year) + '.csv'
    if os.path.isfile(filepath) or os.path.isfile('data/index-of-tables.csv'):
        return
    start_time = time.time()
    time1 = start_time
    benefits = pd.read_csv("data/benefits.csv")
    list_temp = []
    iterations = len(benefits['name'])
    index_of_tables = pd.DataFrame(columns = ['catalog', 'name', 'year', 'period', 'id', 'header', 'type', 'link'])
    for i in range(iterations):
        if (i % 100 == 0):
            print('index-of-tables-' + str(year) + ': ' + str(round(i*100/iterations, 1)) + '%')
        name = benefits['name'][i]
        name_parsed = urllib.parse.quote(name)
        catalog = benefits['catalog'][i]
        list_temp.clear()
        table_number = 0
        data_exist = False
        is_periods_data = False
        path = 'https://api.nfz.gov.pl/app-stat-api-jgp/index-of-tables?catalog=' + catalog + '&format=json&api-version=1.0&name=' + name_parsed
        delta = time.time() - time1
        json_file = get_html(path, delta)
        time1 = time.time()
        if (json_file['data'] != None):
            years_number = len(json_file['data']['attributes']['years'])
            for k in range(years_number):
                data_year = json_file['data']['attributes']['years'][k]['year']
                if (data_year == year):
                    data_exist = True
                    table_number = k
                    if (type(json_file['data']['attributes']['years'][k]['periods']) == list): # Is data period or full-year
                        is_periods_data = True
                    else:
                        is_periods_data = False
        if (data_exist):
            json_file_subdata = json_file['data']['attributes']['years'][table_number]
            if (not is_periods_data):
                for j in range(len(json_file_subdata['tables'])):
                    table_header = json_file_subdata['tables'][j]['attributes']['header']
                    table_id = json_file_subdata['tables'][j]['id']
                    table_type = json_file_subdata['tables'][j]['type']
                    table_link = json_file_subdata['tables'][j]['links']['related']
                    period = str(year)
                    list_temp.append([catalog, name, year, period, table_id, table_header, table_type, table_link])
            else:
                for j in range(len(json_file_subdata['periods'][0]['tables'])):
                    table_header = json_file_subdata['periods'][0]['tables'][j]['attributes']['header']
                    table_id = json_file_subdata['periods'][0]['tables'][j]['id']
                    table_type = json_file_subdata['periods'][0]['tables'][j]['type']
                    table_link = json_file_subdata['periods'][0]['tables'][j]['links']['related']
                    date_from = json_file_subdata['periods'][0]['date-from']
                    date_to = json_file_subdata['periods'][0]['date-to']
                    period = date_from + '-' + date_to
                    list_temp.append([catalog, name, year, period, table_id, table_header, table_type, table_link])
            df = pd.DataFrame(list_temp, columns = ['catalog', 'name', 'year', 'period', 'id', 'header', 'type', 'link'])
            index_of_tables = index_of_tables.append(df)
    index_of_tables = index_of_tables.drop_duplicates()
    index_of_tables.to_csv(filepath, index = False)   
    print('Runtime - index-of-tables-' + str(year) + ': ' + str(round(time.time() - start_time, 2)))

def medical_data(year, table_type): # Download medical data
    filepath = 'data/annual/' + table_type + '-' + str(year) + '.csv'
    if os.path.isfile(filepath) or os.path.isfile(table_type + '.csv'):
        return
    index_of_tables = pd.read_csv('data/index-of-tables.csv')
    df = index_of_tables.loc[(index_of_tables['type'] == table_type) & (index_of_tables['year'] == year)][['name', 'catalog', 'year', 'period', 'link']]
    index_list = list(df.index.values)
    start_time = time.time()
    time1 = start_time
    not_empty = True
    iterations = len(index_list)
    table_number = 0
    first_not_empty = False
    for i in index_list:
        table_number += 1
        data_link = df['link'][i]
        not_empty = True
        page = 0
        if (table_number % 50 == 1):
            print(table_type + '-' + str(year) + ': ' + str(round(table_number*100/iterations, 1)) + '%')
        while(not_empty):
            page += 1
            path = 'https://api.nfz.gov.pl/app-stat-api-jgp' + data_link + '?page=' + str(page) + '&limit=25&format=json&api-version=1.0'
            delta = time.time() - time1
            json_file = get_html(path, delta)
            time1 = time.time()
            not_empty = ('data' in json_file)
            if (not_empty):
                if (table_type == 'histograms'): # Special case - another JSON file structure
                    df1 = pd.DataFrame(json_file['data']['attributes']['data'][0]['points'])
                    not_empty = False
                else:
                    df1 = pd.DataFrame(json_file['data']['attributes']['data'])
                df1['name'] = df['name'][i]
                df1['catalog'] = df['catalog'][i]
                df1['year'] = df['year'][i]
                df1['period'] = df['period'][i]
                if (not first_not_empty):
                    first_not_empty = True
                    medical_data = df1
                else:                
                    medical_data = medical_data.append(df1)
    medical_data = medical_data.drop_duplicates()
    medical_data.to_csv(filepath, index = False)
    print('Runtime - ' + table_type + '-' + str(year) + ': ' + str(round(time.time() - start_time, 2))) 

# =============================================================================
# Main
# =============================================================================

if not os.path.isdir('data/annual'):
    try:
        os.makedirs('data/annual')
    except OSError:
        print ("Creation of the directory failed")
        sys.exit()

# Downloading data and creating the table 'benefits.csv'
benefits() 

# Downloading data and creating the table 'index-of-tables.csv'
filenames = []
filepath = 'data/index-of-tables.csv'
if not os.path.isfile(filepath):
    for year in year_list:
        index_of_tables(year)
        filenames.append('data/annual/index-of-tables-' + str(year) + '.csv')
    pd.concat([pd.read_csv(f) for f in filenames]).to_csv('data/index-of-tables.csv', index=False )

# Downloading data and creating tables with medical data
table_list = ['general-data', 'hospitalization-by-age', 'hospitalization-by-gender', 'hospitalization-by-admission', 'hospitalization-by-discharge', 'histograms', 'icd-9-procedures', 'icd-10-diseases', 'product-categories', 'hospitalization-by-service', 'hospitalization-by-admission-nfz']
for year in year_list:
    for table in table_list:
        medical_data(year, table)
    
# Joining tables
for table_name in table_list:
    filenames = []
    filepath = 'data/' + table_name + '.csv'
    if not os.path.isfile(filepath):
        for year in year_list:
            filenames.append('data/annual' + table_name + '-' + str(year) + '.csv') 
        pd.concat([pd.read_csv(f) for f in filenames]).to_csv('data/' + table_name + '.csv', index=False )