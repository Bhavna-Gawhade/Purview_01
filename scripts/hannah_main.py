##! /usr/bin/env python3


# Import Functions
# ---------------
from modules import entity, collection, glossary
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *



# Import Packages
# ---------------
from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
from utils import get_credentials, create_purview_client
import json


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------


# Main Function
# ---------------

def main():
    print()

    '''
    profit_center_regex = r"/\b.*Profit[^A-Za-z0-9]?(Center|CTR).*\b/|Profit[^A-Za-z0-9]?(Center|CTR)"
    storage_location_regex = r"/\b.*Storage[^A-Za-z0-9]?(Location|LOC).*\b/|Storage[^A-Za-z0-9]?(Location|LOC)|/\b.*Warehouse.*\b/|Warehouse|/\b.*SLOC.*\b/|SLOC"
    '''
    
    '''
    pass_file_names = generate_all_pass_test_files(CLASSIFICATION_EXCEL_FILE, MAPPINGS_EXCEL_FILE)
    print(pass_file_names)
    '''

    '''
    valuation_class_pass_file_name = 'test_CSVs/to_pass/material_type_to_pass_test_column_names.csv'
    column_names = get_csv_column_names(valuation_class_pass_file_name)
    print(column_names)
    print(len(column_names))
    '''

    """

    classification_name = "Division"
    glossary_term_name = "Division"
    result = associate_classification_and_glossary_term(classification_name, glossary_term_name)
    print(result)

    """

    file_path = "Classifications_from_Glossary_Terms.xlsx"
    classification_info_sheet_name = "TERM_INFO"
    abbreviation_mappings_sheet_name = "ABBREVIATION_MAPPINGS"

    all_regex = generate_all_regex(file_path, classification_info_sheet_name, abbreviation_mappings_sheet_name)

    export_to_excel(all_regex, "all_regex_terms.xlsx")

    print()



if __name__ == '__main__':
    main()
