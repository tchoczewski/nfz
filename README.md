# National Health Fund of Poland (Narodowy Fundusz Zdrowia, NFZ) – Healthcare Statistics

This repository provides structured access to publicly available hospitalization statistics published by the National Health Fund of Poland (NFZ). The data is retrieved via the official NFZ API and organized for further analysis, research, and exploratory data science work.

---

## Project Purpose

The goal of this project is to automate the collection and organization of NFZ hospitalization data into machine-readable tables that can be easily used for:

- healthcare analytics and reporting  
- epidemiological and public health research  
- policy analysis  
- exploratory data analysis (EDA)  
- educational and academic purposes  

---

## Data Source

The National Health Fund of Poland provides API access to comprehensive medical statistics:

- **API Documentation**:  
  https://api.nfz.gov.pl/app-stat-api-jgp  

- **Statistics Portal (manual exploration)**:  
  https://statystyki.nfz.gov.pl/Benefits  

All data originates from publicly available NFZ resources.

---

## Data Download

This repository contains a Python script that automates downloading data from the NFZ API:

- **Download script**:  
  https://github.com/tchoczewski/nfz/blob/master/download_data.py  

Downloaded data is stored in the following directory:

- **Downloaded data**:  
  https://github.com/tchoczewski/nfz/tree/master/data  

For convenience, the combined dataset for all available years has been compressed into a single archive:

- **Combined data (ZIP)**:  
  https://github.com/tchoczewski/nfz/raw/master/data/joined_tables.zip  

---

## Usage

### Requirements
- Python 3.8+
- Standard Python data stack (e.g. `requests`, `pandas`)

### Running the downloader

```bash
python download_data.py
```

The script automatically:
1. Retrieves metadata tables required for further downloads
2. Iterates through all available years and DRG/JGP codes
3. Saves downloaded tables into the `data/` directory

---

## Data Format

- File format: **CSV**
- Encoding: **UTF-8**
- Delimiter: **comma (`,`)**
- One file per year and data category

---

## Data Structure

For each year and diagnosis-related group (DRG, Polish: *Jednorodne Grupy Pacjentów – JGP*), the data is aggregated into the following categories:

- **`general-data`** – General statistics such as number of patients and hospitalizations.
- **`histograms`** – Distribution of hospitalizations by length of stay (0–50 days).
- **`hospitalization-by-admission-nfz`** – Hospitalizations categorized by NFZ-specific admission reasons.
- **`hospitalization-by-admission`** – Hospitalizations categorized by general admission reasons.
- **`hospitalization-by-age`** – Hospitalizations broken down by patient age groups.
- **`hospitalization-by-discharge`** – Hospitalizations categorized by discharge reasons.
- **`hospitalization-by-gender`** – Hospitalizations categorized by patient gender.
- **`hospitalization-by-service`** – Hospitalizations categorized by contract/service type (NFZ-specific).
- **`icd-10-diseases`** – Diagnosed diseases classified according to ICD-10.
- **`icd-9-procedures`** – Medical procedures classified according to ICD-9.
- **`product-categories`** – Hospitalizations categorized by NFZ product types.

---

## Supporting Tables

At the beginning of the download process, the script retrieves two auxiliary tables required for proper data collection:

- **`benefits`** – A dictionary containing all DRG (JGP) codes available in the NFZ system.
- **`index-of-tables`** – Identification numbers and download links for all available statistical tables.

---

## Coverage

- **Geography**: Poland (national level)  
- **Data type**: Hospital inpatient care  
- **Time coverage**: depends on NFZ availability (multiple consecutive years)

---

## Project Status

The repository focuses on data collection and structuring.  
Data availability and updates depend on the NFZ API.

---

## License and Disclaimer

This project uses publicly available data published by the National Health Fund of Poland (NFZ).

- The repository is provided for **research and educational purposes**.
- The author does not guarantee data completeness or correctness.
- Users are responsible for complying with any terms defined by the original data provider (NFZ).
