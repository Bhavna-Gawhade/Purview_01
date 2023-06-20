##! /usr/bin/env python3


# Import Functions
# ---------------
from modules import entity, collection
from modules.classification.classification_test_case_generator import *
from modules.classification.classification_regex_generator import *
from modules.classification.shared_generator_functions import *



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

CLASSIFICATION_EXCEL_FILE = "Classification_Regex_Rules.xlsx"
MAPPINGS_EXCEL_FILE = "Keyword_to_Common_Abbreviation_Mappings.xlsx"


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

    '''
    all_regex = generate_all_regex(CLASSIFICATION_EXCEL_FILE, MAPPINGS_EXCEL_FILE)
    print(all_regex)
    '''

    all_type_defs = CLIENT.get_all_typedefs()
    entity_defs = all_type_defs["entityDefs"]
    all_type_names = []

    for entity in entity_defs:
        rel_attr_defs = entity["relationshipAttributeDefs"]
        for td in rel_attr_defs:
            all_type_names.append(td["relationshipTypeName"])
    unique_type_names = list(set(all_type_names))

    sap_types = []
    for name in unique_type_names:
        if "sap" in name:
            sap_types.append(name)
        
    sap_s4hana_types = []
    for name in sap_types:
        if "sap_s4hana" in name:
            sap_s4hana_types.append(name)
    print(sap_s4hana_types)


    




if __name__ == '__main__':
    main()
