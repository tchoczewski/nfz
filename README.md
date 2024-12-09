# National Health Fund of Poland (Narodowy Fundusz Zdrowia, NFZ) Healthcare Statistics

## Data Source

The National Health Fund of Poland provides API access to comprehensive medical statistics:  
[API Documentation](https://api.nfz.gov.pl/app-stat-api-jgp)  

Additionally, some data can be manually explored here:  
[NFZ Statistics Portal](https://statystyki.nfz.gov.pl/Benefits)  

## Data Download

This repository contains a Python script to automate the downloading of data from the NFZ API. The script can be found here:  
[Download Script](https://github.com/tchoczewski/nfz/blob/master/download_data.py)  

The data for the years 2009-2023 is saved in the following directory:  
[Downloaded Data](https://github.com/tchoczewski/nfz/tree/master/data)  

Additionally, the combined data for all years (2009-2023) has been compressed into a single ZIP file:  
[Download Combined Data (ZIP)](https://github.com/tchoczewski/nfz/blob/master/data/joined_tables.zip)

## Data Structure

For each year and diagnosis-related group (DRG, Polish: Jednorodne Grupy Pacjentów, JGP), the data is aggregated into various categories, including:  

- **`general-data`**: General information, such as the number of patients or hospitalizations.  
- **`histograms`**: Distribution of hospitalizations by length of stay (0–50 days).  
- **`hospitalization-by-admission-nfz`**: Hospitalizations categorized by the reason for admission (NFZ-specific classification).  
- **`hospitalization-by-admission`**: Hospitalizations categorized by admission reasons.  
- **`hospitalization-by-age`**: Hospitalizations broken down by patient age groups.  
- **`hospitalization-by-discharge`**: Hospitalizations categorized by discharge reasons.  
- **`hospitalization-by-gender`**: Hospitalizations categorized by gender.  
- **`hospitalization-by-service`**: Hospitalizations categorized by contract type (NFZ-specific classification).  
- **`icd-10-diseases`**: Diagnosed diseases categorized by ICD-10 classification.  
- **`icd-9-procedures`**: Medical procedures categorized by ICD-9 classification.  
- **`product-categories`**: Hospitalizations categorized by product type (NFZ-specific classification).  

### Supporting Tables  

The script also downloads two additional tables at the start of the process, which are essential for data retrieval:  
- **`benefits`**: A dictionary containing all DRG codes.  
- **`index-of-tables`**: Identification numbers and download links for all available tables.
