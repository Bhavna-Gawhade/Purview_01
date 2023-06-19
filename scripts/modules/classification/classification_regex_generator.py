##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from modules.classification.shared_generator_functions import *


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

def generate_regex_partial(keyword: str, mapping: dict, word: str):
    abbreviations = mapping["abbreviations"]
    crafted_str = "(" + word
    for abbrev in abbreviations:
        crafted_str = crafted_str + "|" + abbrev
    crafted_str = crafted_str + ")" + "[^A-Za-z0-9]"
    regex_partial = keyword.replace(word, crafted_str)
    return regex_partial

def create_regex_pipes(keywords: list, mappings: dict):
    storage_location_regex = r"/\b.*Storage[^A-Za-z0-9]?(Location|LOC).*\b/|Storage[^A-Za-z0-9]?(Location|LOC)|/\b.*Warehouse.*\b/|Warehouse|/\b.*SLOC.*\b/|SLOC"
    pipe0 = r"/\b.*Storage[^A-Za-z0-9]?(Location|LOC).*\b/"
    pipe1 = r"Storage[^A-Za-z0-9]?(Location|LOC)"
    pipe2 = r"/\b.*Warehouse.*\b/"
    pipe3 = r"Warehouse"
    pipe4 = r"/\b.*SLOC.*\b/"
    pipe5 = r"SLOC"


    testing_alt_storage_location_regex = r"/\b.*Storage[^A-Za-z0-9]?(Location|LOC).*\b/|/\b.*Warehouse.*\b/|/\b.*SLOC.*\b/"

    regex_partials = []

    
    

    mapping_dict = {mapping['word']: mapping['abbreviations'] for mapping in mappings}

    for keyword in keywords:
        # create two pipes

        # if the keyword has an abbreviation mapping in it, handle here
        replaced_string = keyword
    
        for key, value in mapping_dict.items():
            replaced_string = replaced_string.replace(key, value)

        '''
        words = keyword.split()
        for word in words:
            for mapping in mappings:
                if mapping['word'] in word:
                    regex_partial = generate_regex_partial(keyword, mapping, word)

                    print(regex_partial)

                    regex_partials.append(regex_partial)
                # if not, handle here
        ''' 

    print("hereee")
    raise Exception


def create_regex(classification: dict, mappings: list):
    keywords = classification["keywords"]
    regex = create_regex_pipes(keywords, mappings)
    regex_dict = {
        "classification_name": classification["classification_name"],
        "regex": regex
    }
    return regex_dict


def generate_all_regex(classifications_file_path: str, mappings_file_path: str):
    all_regex = []
    classifications = process_classifications_file(classifications_file_path)
    mappings = process_mappings_file(mappings_file_path)
    for c in classifications:
        regex_dict = create_regex(c, mappings)
        all_regex.append(regex_dict)
        
    return all_regex
    


# Main Processing
# ---------------

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()


