# Script to download healthcare data from the National Health Fund of Poland
# (NFZ) API.
# The script collects comprehensive statistics on healthcare services,
# focusing on Diagnosis-Related Groups (DRG), patient demographics, diagnoses
# and medical procedures. It automates the process of fetching and storing data
# for multiple years.
# API reference: https://api.nfz.gov.pl/app-stat-api-jgp

import requests
import pandas as pd
import time
import urllib.parse
import os
import sys


# =============================================================================
# Constants
# =============================================================================

# API version used for the requests
API_VERSION = "1.1"

# Minimum delay between consecutive API requests to comply with NFZ rate limits
TIME_API = 0.1  # 10 requests per second, i.e., 0.1 seconds between requests

# Maximum number of request attempts for a single URL
MAX_ATTEMPTS = 5


# =============================================================================
# Parameters
# =============================================================================

# Years to download data for
years = [2021, 2022, 2023]

# List of tables to download data for
tables = [
    "general-data",
    "hospitalization-by-age",
    "hospitalization-by-gender",
    "hospitalization-by-admission",
    "hospitalization-by-discharge",
    "histograms",
    "icd-9-procedures",
    "icd-10-diseases",
    "product-categories",
    "hospitalization-by-service",
    "hospitalization-by-admission-nfz"
]


# =============================================================================
# Utility functions
# =============================================================================

def get_json(path: str, delta: float):
    """Fetch JSON data from a given URL with retry logic."""
    if delta <= TIME_API:
        time.sleep(TIME_API - delta)
    attempts = 0
    while (attempts < MAX_ATTEMPTS):
        try:
            with requests.Session() as ses:
                json_file = ses.get(path).json()
                return json_file
        except requests.exceptions.RequestException as e:
            attempts += 1
            print(f"Attempt {attempts}/{MAX_ATTEMPTS} failed: {e}")
            time.sleep(TIME_API)
    print("Data download failed after multiple attempts. Check your internet "
          "connection or URL.")
    sys.exit(1)


def create_directory(directory_path: str):
    """Ensure that a directory exists, create it if necessary."""
    if not os.path.isdir(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as e:
            print(f"Creation of the {directory_path} directory failed: {e}")
            sys.exit(1)


# =============================================================================
# Data Download Functions
# =============================================================================

def download_medical_data(year: int, table_type: str):
    """Download medical data for a specific year and table type."""
    filepath = f"data/annual/{table_type}-{year}.csv"
    if os.path.isfile(filepath):
        return

    index_of_tables = pd.read_csv("data/index-of-tables.csv")
    df = index_of_tables.loc[(index_of_tables["type"] == table_type) &
                             (index_of_tables["year"] == year)
                             ][["name", "catalog", "year", "period", "link"]]
    index_list = list(df.index.values)
    start_time = time.time()
    time1 = start_time
    not_empty = True
    iterations = len(index_list)
    table_number = 0
    first_not_empty = False
    for i in index_list:
        table_number += 1
        data_link = df["link"][i]
        not_empty = True
        page = 0
        if (table_number % 10 == 1 or table_number == iterations):
            print(f"\r{table_type}-{year}: {round(table_number * 100 / iterations, 1)}%", end="")
        while not_empty:
            page += 1
            path = f"{data_link}&page={page}&limit=25&api-version={API_VERSION}"
            delta = time.time() - time1
            json_file = get_json(path, delta)
            time1 = time.time()
            not_empty = ("data" in json_file)
            if (not_empty):
                # Special case - another JSON file structure
                if (table_type == "histograms"):
                    df1 = pd.DataFrame(
                        json_file["data"]["attributes"]["data"][0]["points"])
                    not_empty = False
                else:
                    df1 = pd.DataFrame(json_file["data"]["attributes"]["data"])
                df1["name"] = df["name"][i]
                df1["catalog"] = df["catalog"][i]
                df1["year"] = df["year"][i]
                df1["period"] = df["period"][i]
                if (not first_not_empty):
                    first_not_empty = True
                    medical_data = df1
                else:
                    medical_data = pd.concat([medical_data, df1],
                                             ignore_index=True)
    medical_data = medical_data.drop_duplicates()
    medical_data.to_csv(filepath, index=False)
    print(f"\nRuntime - {table_type}-{year}: {round(time.time() - start_time, 2)} s\n")


def download_benefits():
    """Download and save benefits catalog."""
    filepath = "data/benefits.csv"
    if os.path.isfile(filepath):
        return

    start_time = time.time()
    time1 = start_time
    catalogs = ["1a", "1b", "1c", "1d", "1w"]
    benefits = pd.DataFrame(columns=["code", "name", "catalog"])
    for catalog in catalogs:
        page = 0
        while True:
            page += 1
            url = (
                f"https://api.nfz.gov.pl/app-stat-api-jgp/benefits"
                f"?benefit=%%%&catalog={catalog}&format=json&limit=25"
                f"&api-version={API_VERSION}&page={page}"
            )
            delta = time.time() - time1
            json_data = get_json(url, delta)
            time1 = time.time()
            if not json_data["data"]:
                break

            df = pd.json_normalize(json_data["data"])
            df["catalog"] = catalog
            benefits = pd.concat([benefits, df], ignore_index=True)
    benefits = benefits.drop_duplicates()
    benefits.to_csv(filepath, index=False)
    print(f"Runtime - benefits: {round(time.time() - start_time, 2)} s\n")


def download_index_of_tables(years):
    """Download and save the index of all available tables."""
    filenames = []
    for year in years:
        filepath = f"data/annual/index-of-tables-{year}.csv"
        if os.path.isfile(filepath):
            continue

        start_time = time.time()
        time1 = start_time
        benefits = pd.read_csv("data/benefits.csv")
        list_temp = []
        iterations = len(benefits["name"])
        index_of_tables = pd.DataFrame(columns=["catalog", "name", "year",
                                                "period", "id", "header",
                                                "type", "link"])
        for i in range(iterations):
            if (i % 10 == 0 or i == iterations - 1):
                print(f"\rindex-of-tables-{year}: {round((i + 1) * 100 / iterations, 1)}%", end="")
            name = benefits["name"][i]
            name_parsed = urllib.parse.quote(name)
            catalog = benefits["catalog"][i]
            list_temp.clear()
            table_number = 0
            data_exist = False
            is_periods_data = False
            path = (
                f"https://api.nfz.gov.pl/app-stat-api-jgp/index-of-tables"
                f"?catalog={catalog}&format=json&api-version={API_VERSION}"
                f"&name={name_parsed}"
            )
            delta = time.time() - time1
            json_file = get_json(path, delta)
            time1 = time.time()
            if (json_file["data"] is not None):
                years_number = len(json_file["data"]["attributes"]["years"])
                for k in range(years_number):
                    data_year = json_file["data"]["attributes"]["years"][k]["year"]
                    if (data_year == year):
                        data_exist = True
                        table_number = k
                        # Is data period or full-year
                        is_periods_data = isinstance(json_file["data"][
                            "attributes"]["years"][k]["periods"], list)
            if (data_exist):
                json_file_subdata = json_file["data"]["attributes"]["years"][table_number]
                if (not is_periods_data):
                    for j in range(len(json_file_subdata["tables"])):
                        table_header = json_file_subdata["tables"][j]["attributes"]["header"]
                        table_id = json_file_subdata["tables"][j]["id"]
                        table_type = json_file_subdata["tables"][j]["type"]
                        table_link = json_file_subdata["tables"][j]["links"]["related"]
                        period = str(year)
                        list_temp.append([catalog, name, year, period,
                                          table_id, table_header, table_type,
                                          table_link])
                else:
                    for j in range(len(json_file_subdata["periods"][0]["tables"])):
                        table_header = json_file_subdata["periods"][0]["tables"][j]["attributes"]["header"]
                        table_id = json_file_subdata["periods"][0]["tables"][j]["id"]
                        table_type = json_file_subdata["periods"][0]["tables"][j]["type"]
                        table_link = json_file_subdata["periods"][0]["tables"][j]["links"]["related"]
                        date_from = json_file_subdata["periods"][0]["date-from"]
                        date_to = json_file_subdata["periods"][0]["date-to"]
                        period = date_from + "-" + date_to
                        list_temp.append([catalog, name, year, period,
                                          table_id, table_header, table_type,
                                          table_link])
                df = pd.DataFrame(list_temp,
                                  columns=["catalog", "name", "year", "period",
                                           "id", "header", "type", "link"])
                index_of_tables = pd.concat([index_of_tables, df],
                                            ignore_index=True)
        index_of_tables = index_of_tables.drop_duplicates()
        index_of_tables.to_csv(filepath, index=False)
        print(f"\nRuntime - index-of-tables-{year}: {round(time.time() - start_time, 2)} s\n")
        filenames.append(f"data/annual/index-of-tables-{year}.csv")
    if filenames:
        pd.concat([pd.read_csv(f) for f in filenames]).to_csv(
            "data/index-of-tables.csv")


def download_selected_medical_tables(years, tables):
    """Download medical data for selected years and tables."""
    for year in years:
        for table in tables:
            download_medical_data(year, table)


def join_tables(years, tables):
    """Join tables for all years."""
    for table in tables:
        filenames = []
        for year in years:
            filenames.append(f"data/annual/{table}-{year}.csv")
        pd.concat(
            [pd.read_csv(f) for f in filenames]).to_csv(f"data/{table}.csv",
                                                        index=False)


# =============================================================================
# Main Execution
# =============================================================================

def main():
    """Main function to orchestrate data download."""
    create_directory("data")
    create_directory("data/annual")

    download_benefits()
    download_index_of_tables(years)
    download_selected_medical_tables(years, tables)
    join_tables(years, tables)

    print("Data download successful!")


if __name__ == "__main__":
    main()
