# National Health Fund of Poland (polish: Narodowy Fundusz Zdrowia, NFZ) medical statistics for years 2009-2019

## Data source
National Health Fund of Poland provides API access to medical data: \
https://api.nfz.gov.pl/app-stat-api-jgp \
Some data can also be searched manually here: \
https://statystyki.nfz.gov.pl/Benefits

## Data download
I wrote a Python script to download the data, it can be found in the current github repository: \
https://github.com/tchoczewski/nfz/blob/master/download_data.py \
All downloaded data can be found here: \
https://github.com/tchoczewski/nfz/tree/master/data

## Data structure
For given year and diagnosis-related group (DRG, polish: Jednorodne Grupy Pacjentów, JGP) data are aggregated in some categories:
* __general-data:__ consists of general information like number of patients/hospitalizations
* __histograms:__ number of hospitalizations by days of stay (0-50 days)
* __hospitalization-by-admission-nfz:__ number of hospitalizations by the reason for admission to the hospital (NFZ categorization)
* __hospitalization-by-admission:__ number of hospitalizations by the reason for admission to the hospital
* __hospitalization-by-age:__ number of hospitalizations by patient age group (<1, 1-6, 7-17, 18-40, 41-60, 61-80, >80)
* __hospitalization-by-discharge:__ number of hospitalizations by the reason for discharge from the hospital
* __hospitalization-by-gender:__ number of hospitalizations by patient gender (kobieta: female, mężczyzna: male)
* __hospitalization-by-service:__ number of hospitalizations by contract type (NFZ specific)
* __icd-10-diseases:__ number of diagnosis of diseases of diseases in ICD-10 classification
* __icd-9-procedures:__ number of medical procedures in ICD-9 classification
* __product-categories:__ number of hospitalizations by category type (NFZ specific)

A given hospitalization can be classified into only one DRG group. There are two additional tables containing information necessary to download the data (these tables are downloaded by the script at the beginning):
* __benefits:__ dictionary with all DRG codes
* __index-of-tables:__ identification numbers and links to all available tables in database

## Example
If we choose year 2019 and DRG group called "A86 CHOROBY NEURONU RUCHOWEGO" we will see the following information in selected tables:

### hospitalization-by-age
 | branch | hospital-types | age-group-code | age-group-name | number-of-hospitalizations | percentage | duration-of-hospitalization-mediana | name | catalog | year | period | 
 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
 |  |  | 1 | poniżej 1 | 29 | 1,6 | 1 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 2 | 1 - 6 | 129 | 7,13 | 1 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 3 | 7 - 17 | 126 | 6,96 | 1 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 4 | 18 - 40 | 250 | 13,81 | 1 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 5 | 41 - 60 | 423 | 23,37 | 4 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 6 | 61 - 80 | 802 | 44,31 | 5 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 7 | 81 i więcej | 51 | 2,82 | 7 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 8 | brak danych | 0 | 0 | 0 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 

### hospitalization-by-gender
 | branch | hospital-types | gender-code | gender-name | number-of-hospitalizations | percentage | duration-of-hospitalization-mediana | name | catalog | year | period | 
 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
 |  |  | 0 | płeć nieokreślona | 0 | 0 | 0 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 9 | nieznana | 0 | 0 | 0 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 2 | kobieta | 825 | 45,58 | 3 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 |  |  | 1 | mężczyzna | 985 | 54,42 | 4 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 

### icd-10-diseases
 | disease-code | disease-name | number-of-hospitalizations | percentage | duration-of-hospitalization-mediana | name | catalog | year | period | 
 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
 | G12.2 | Stwardnienie boczne zanikowe | 1016 | 56,13 | 5 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 | G12.1 | Inne dziedziczne zaniki mięśni pochodzenia rdzeniowego | 299 | 16,52 | 0 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 | G12.9 | Zanik mięśni pochodzenia rdzeniowego, nie określony | 194 | 10,72 | 5 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 | G12.0 | Zanik mięśni pochodzenia rdzeniowego dziecięcy, typu I [Werdniga-Hoffmana] | 184 | 10,17 | 1 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
 | G12.8 | Inne zaniki mięśni pochodzenia rdzeniowego i zespoły pokrewne | 117 | 6,46 | 5 | A86 CHOROBY NEURONU RUCHOWEGO | 1a | 2019 | 2019 | 
