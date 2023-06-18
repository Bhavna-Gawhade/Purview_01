##! /usr/bin/env python3


# Function Imports
# ---------------
from modules import entity
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------
from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
import json
import csv
from pathlib import Path
import pandas as pd

# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
CLASSIFICATION_EXCEL_FILE = "Classification_Regex_Rules.xlsx"

# Functions
# ---------------

def process_classifications_file(file_path):
    file = pd.read_excel(file_path)
    classifications_dict = []
    for row in file.iterrows():
        x = {
            "classification_name": row["Classification_Name"],
            "keywords": row['Keywords'].split(","),
            "common_abbreviations": row['Common_Abbreviations'].split(",")
        }
        classifications_dict.append(x)
    return classifications_dict


def process_mappings_file(file_path):
    file = pd.read_excel(file_path)
    mappings = []
    for row in file.iterrows():
        abbreviations_str = row['Abbreviations']
        abbreviations = [word.strip() for word in abbreviations_str.split(",")]
        x = {
            "word": row['Word'],
            "abbreviations": abbreviations
        }
        mappings.append(x)
    return mappings


def get_all_variations_of_keyword(keyword: str, mappings: list):
    variations = []
    variations.append(keyword)
    for word in keyword:
        abbreviations_of_word = mappings["word"]
        for x in abbreviations_of_word:
            name = ""


def create_names_from_keywords(classification: dict, mappings: list):
    names = []
    for keyword in classification["keywords"]:
        all_variations_of_keyword = get_all_variations_of_keyword(keyword, mappings)
        # test cases for full name

        # test cases for abbreviations substituted in
        print()
    print()


def generate_variations(keywords, mapping):
    if not keywords:
        return ['']
    
    keyword = keywords[0]
    abbreviations = mapping.get(keyword, [keyword])
    
    variations = []
    remaining_variations = generate_variations(keywords[1:], mapping)
    
    for abbreviation in abbreviations:
        for variation in remaining_variations:
            variations.append(abbreviation + ' ' + variation)
    
    return variations


def create_testing_column_names(classifications_file_path: str, mappings_file_path: str):
    column_names = []
    classifications = process_classifications_file(classifications_file_path)
    mappings = process_mappings_file(mappings_file_path)
    testing_column_names = []
    for c in classifications:
        names = create_names_from_keywords(c, mappings)
        testing_column_names.append(names)

    

def get_excel_column_names(file_path):
    df = pd.read_excel(file_path)
    column_names = df.columns.tolist()
    return column_names


def generate_test_case_csv_file(keywords: list, common_abbreviations: list):
    # Specify the column names
    column_names = ['Column1', 'Column2', 'Column3']

    # Specify the data rows
    data_rows = [
        [1, 'A', True],
        [2, 'B', False],
        [3, 'C', True]
    ]

    # Specify the output file name
    filename = 'output.csv'

    # Open the CSV file in write mode
    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the column names
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(data_rows)

    print(f'CSV file "{filename}" created successfully.')


# Main Processing
# ---------------

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()