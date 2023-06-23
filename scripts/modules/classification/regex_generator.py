##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from modules.classification.shared_generator_functions import *


# Package Imports
# ---------------

from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
from pathlib import Path
import pandas as pd


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def handle_word(word: str, mappings_dict: dict):
    word_component = ""
    if word in mappings_dict:
        abbreviations = mappings_dict[word]
        word_component = f"({'|'.join([word] + abbreviations)})"
    else:
        word_component = "(" + word + ")"
    return word_component


def create_regex_string(keywords: list, mappings_dict: dict):
    regex_components = []
    for keyword in keywords:
        keyword_components = [handle_word(word, mappings_dict) for word in keyword.split()]
        regex_components.append("[^A-Za-z0-9]?".join(keyword_components) + ".*") 
    regex_string = ".*" + "|.*".join(regex_components)
    return regex_string


def get_regex_dict(classification: dict, mappings_dict: dict):
    keywords = classification["keywords"]
    regex = create_regex_string(keywords, mappings_dict)
    regex_dict = {
        "classification_name": classification["classification_name"],
        "glossary_term": classification["glossary_term"],
        "keywords": keywords,
        "regex": regex
    }
    return regex_dict


def generate_all_regex(excel_file_path: str, classification_sheet_name: str, mappings_sheet_name: str):
    all_regex_dicts = []
    classifications = process_classifications_sheet(excel_file_path, classification_sheet_name)
    mappings = process_mappings_sheet(excel_file_path, mappings_sheet_name)
    mappings_dict = {mapping['word']: mapping['abbreviations'] for mapping in mappings}

    for c in classifications:
        regex_dict = get_regex_dict(c, mappings_dict)
        all_regex_dicts.append(regex_dict)
        
    return all_regex_dicts


def export_to_excel(all_regex_dicts, file_path):
    data = []
    for regex_dict in all_regex_dicts:
        classification_name = regex_dict["classification_name"]
        keywords = ", ".join(regex_dict["keywords"])
        regex = regex_dict["regex"]
        data.append([classification_name, keywords, regex])
    
    df = pd.DataFrame(data, columns=["Classification_Name", "Keywords", "REGEX"])
    df.to_excel(file_path, index=False)
    

# Main Processing
# ---------------

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()


