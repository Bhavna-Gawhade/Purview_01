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
import re
import random
import string
import os


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def process_classifications_file(file_path):
    file = pd.read_excel(file_path)
    classifications_dict = []
    for index, row in file.iterrows():
        x = {
            "classification_name": row["Classification_Name"],
            "keywords": row['Keywords'].split(",")
            #"common_abbreviations": row['Common_Abbreviations'].split(",")
        }
        classifications_dict.append(x)
    return classifications_dict


def process_mappings_file(file_path):
    file = pd.read_excel(file_path)
    mappings = []
    for index, row in file.iterrows():
        abbreviations_str = row['Abbreviations']
        abbreviations = [word.strip() for word in abbreviations_str.split(",")]
        x = {
            "word": row['Word'],
            "abbreviations": abbreviations
        }
        mappings.append(x)
    return mappings


def generate_variations(keywords, mappings):
    variations = set(keywords)
    for keyword in keywords:
        for mapping in mappings:
            word = mapping['word']
            abbreviations = mapping['abbreviations']
            if word in keyword:
                mapping_variations = [keyword.replace(word, abbreviation) for abbreviation in abbreviations]
                variations.update(mapping_variations)
                variations.add(keyword)
                #variations.update(abbreviations)
                variations.update(generate_variations(mapping_variations, mappings))
    return list(variations)


def get_keyword_variations(classification: dict, mappings: list):
    keywords = classification["keywords"]
    variations = generate_variations(keywords, mappings)
    stripped_variations = strip_strings(variations)
    unique_variations = []
    for variation in stripped_variations:
        if not any(variation.startswith(abbreviation) for abbreviation in mappings[0]['abbreviations']):
            unique_variations.append(variation)
    
    unique_variations = list(set(unique_variations))
    return unique_variations


def get_excel_column_names(file_path):
    df = pd.read_excel(file_path)
    column_names = df.columns.tolist()
    return column_names


def get_csv_column_names(file_name):
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        column_names = next(reader)  # Read the first row
    return column_names


def to_snake_case(input_str: str):
    snake_case_string = input_str.replace(' ', '_')
    snake_case_string = snake_case_string.lower()
    return snake_case_string


def create_test_case_csv_file(classification_name: str, to_pass_or_fail: str, column_names: list):
    directory = 'test_CSVs/to_pass'
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    snake_case_classification_name = to_snake_case(classification_name)
    file_name_without_path = snake_case_classification_name + '_' + to_pass_or_fail + '_test_column_names.csv'
    file_name = os.path.join(directory, file_name_without_path)

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerow(['0'] * len(column_names))

    print(f'CSV file "{file_name}" created successfully.')
    return file_name


def get_all_spacings_between(variations: list):
    all_spacings = []
    special_chars = ['!', '&', '*', '+', '.', '-', '/', ':', '_', '~', "|"]  # Add more special characters if desired
    for variation in variations:
        current_with_space = variation
        no_space = variation.replace(" ", "")
        with_underscores = variation.replace(" ", "_")
        with_one_special_char = variation.replace(" ", random.choice(special_chars))
        all_spacings.extend([current_with_space, no_space, with_underscores, with_one_special_char])
    return all_spacings



def get_all_letter_cases(variations: list):
    all_cases = []
    for variation in variations:
        current = variation
        all_upper = variation.upper()
        all_lower = variation.lower()
        mixed_case = ''.join([char.upper() if random.choice([True, False]) else char.lower() for char in variation])
        title_case = variation.title()
        all_cases.extend([current, all_upper, all_lower, mixed_case, title_case])

    return all_cases


def get_all_paddings(variations: list):
    all_paddings = []
    special_chars = ['!', '&', '*', '+', '.', '-', '/', ':', '_', '~', "|"]  # Add more special characters if desired

    for variation in variations:
        current = variation
        pad_with_spaces = ' ' + variation + ' '
        pad_with_underscores = '_' + variation + '_'
        pad_with_random_special_chars = random.choice(special_chars) + variation + random.choice(special_chars)
        pad_with_random_letters = random.choice(string.ascii_letters) + variation + random.choice(string.ascii_letters)
        all_paddings.extend([current, pad_with_spaces, pad_with_underscores, pad_with_random_special_chars, pad_with_random_letters])
    
    return all_paddings


def generate_pass_column_names(variations: list):
    # Get all cases for each variation
    all_letter_cases = get_all_letter_cases(variations)
    unique_all_letter_cases = list(set(all_letter_cases))

    # Get all spacings between the words
    all_spacings_between = get_all_spacings_between(unique_all_letter_cases)
    unique_all_spacings_between = list(set(all_spacings_between))

    # Pad the variations
    padded_and_complete_variations = get_all_paddings(unique_all_spacings_between)
    unique_padded_and_complete_variations = list(set(padded_and_complete_variations))

    return unique_padded_and_complete_variations


def strip_strings(strings):
    return [string.strip() for string in strings]


def generate_pass_test_file(classification: dict, mappings: list):
    # Get variations of the keywords
    variations = get_keyword_variations(classification, mappings)

    # Create test cases from the variations
    pass_column_names = generate_pass_column_names(variations)

    # Populate the CSV test file
    pass_file_name = create_test_case_csv_file(classification["classification_name"], "to_pass", pass_column_names)

    # Return the file name
    return pass_file_name


def generate_all_pass_test_files(classifications_file_path: str, mappings_file_path: str):
    pass_test_file_names = []
    classifications = process_classifications_file(classifications_file_path)
    mappings = process_mappings_file(mappings_file_path)
    for c in classifications:
        test_file_name = generate_pass_test_file(c, mappings)
        pass_test_file_names.append(test_file_name)
        
    return pass_test_file_names


# Main Processing
# ---------------

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()