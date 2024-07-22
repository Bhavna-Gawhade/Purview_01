##! /usr/bin/env python3

# Function Imports
# ---------------

from pyapacheatlas.core import AtlasEntity ,AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.readers import ExcelConfiguration,ExcelReader
from utils import get_credentials,create_purview_client
from pyapacheatlas.core.glossary import *

# Imports
# ---------------

import pandas as pd
import json
from pathlib import Path
import random
import string
from datetime import date

# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
qa_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
prod_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

# Function to export all the glossary terms to CSV file
def get_all_glossary_terms(client):
    """
    Retrieves all glossary terms from the client, exports them to a CSV file,
    and handles any exceptions that occur during the export process.

    Args:
        client: The client object used to interact with the glossary API.

    Returns:
        None
    """
    result=client.glossary.get_glossaries(-1,0,"ASC")
    term_guids = [term['termGuid'] for term in result[0]['terms']]
    csv_file = f"./ExportGlossaryFiles/glossary_terms.csv"
    try:
        result=client.glossary.export_terms(term_guids,csv_file )
    except Exception as e:
        print(e)

# Function to replace nan with empty string
def replace_nan_with_empty_string(data):
    """
    Replaces all occurrences of NaN values with empty strings in a list of dictionaries.

    Args:
        data (list): A list of dictionaries where NaN values need to be replaced with empty strings.

    Returns:
        list: The modified list of dictionaries with NaN values replaced by empty strings.
    """
    for item in data:
        for key, value in item.items():
            if pd.isna(value):
                item[key] = ""
    return data

def get_all_glossary_terms_into_variables(client):
    
    """
    Retrieves all glossary terms, processes them into lists of attributes, and handles NaN values.

    Args:
        client: The client object used to interact with the glossary API.

    Returns:
        tuple: A tuple containing the following lists:
            - names (list): A list of glossary term names.
            - definitions (list): A list of glossary term definitions.
            - statuses (list): A list of glossary term statuses.
            - experts (list): A list of glossary term experts.
            - stewards (list): A list of glossary term stewards.
            - domains (list): A list of glossary term domains.
            - equivalent_phrases (list): A list of glossary term equivalent phrases.
            - system_table_fields (list): A list of glossary term system table fields.
    """

    csv_file = f"./ExportGlossaryFiles/glossary_terms.csv"
    
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Convert the DataFrame to a list of dictionaries
    data_list = df.to_dict(orient='records')

    # list of dictionaries
    glossary_terms = []
    for row in data_list:
        glossary_terms.append(row)

    glossary_terms=replace_nan_with_empty_string(glossary_terms)

    # Initialize empty lists for each key
    names = []
    definitions = []
    statuses = []
    experts = []
    stewards = []
    domains = []
    equivalent_phrases = []
    system_table_fields = []

    # Iterate through the list of dictionaries and append values to corresponding lists
    for item in glossary_terms:
        names.append(item.get("Name", None))
        definitions.append(item.get("Definition", None))
        statuses.append(item.get("Status", None))
        experts.append(item.get("Experts", None))
        stewards.append(item.get("Stewards", None))
        domains.append(item.get("[Attribute][Business Glossary]Domain", None))
        equivalent_phrases.append(item.get("[Attribute][Business Glossary]Equivalent Phrases", None))
        system_table_fields.append(item.get("[Attribute][Business Glossary]System-Table-Field", None))

    return 
     