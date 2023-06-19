##! /usr/bin/env python3


# Import Functions
# ---------------
from modules import entity, collection
from modules.classification.classification_test_case_generator import *


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

    pass_file_names = generate_all_pass_test_files(CLASSIFICATION_EXCEL_FILE, MAPPINGS_EXCEL_FILE)
    print(pass_file_names)

    
if __name__ == '__main__':
    main()
