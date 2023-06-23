##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client


# Package Imports
# ---------------

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

def process_classifications_sheet(excel_file_path: str, sheet_name: str):
    classification_sheet = extract_sheet_from_excel(excel_file_path, sheet_name)
    classifications_dict = []
    for index, row in classification_sheet.iterrows():
        x = {
            "classification_name": row["Classification_Name"],
            "glossary_term": row["Associated_Glossary_Terms"],
            "keywords": row['Keywords'].split(",")
        }
        classifications_dict.append(x)
    return classifications_dict


def process_mappings_sheet(excel_file_path: str, sheet_name: str):
    mappings_sheet = extract_sheet_from_excel(excel_file_path, sheet_name)
    mappings = []
    for index, row in mappings_sheet.iterrows():
        abbreviations_str = row['Abbreviations']
        abbreviations = [word.strip() for word in abbreviations_str.split(",")]
        x = {
            "word": row['Word'],
            "abbreviations": abbreviations
        }
        mappings.append(x)
    return mappings


def extract_sheet_from_excel(file_path, sheet_name):
    excel_sheet = pd.read_excel(file_path, sheet_name=sheet_name)
    return excel_sheet


# Main Processing
# ---------------

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()