##! /usr/bin/env python3


# Import Functions
# ---------------
from modules import entity, collection, glossary
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.shared_lineage_functions import *



# Import Packages
# ---------------
from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
from utils import get_credentials, create_purview_client
import json
import datetime


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

    """
    classification_name = "Division"
    glossary_term_name = "Division"
    result = associate_classification_and_glossary_term(classification_name, glossary_term_name)
    print(result)
    """

    """
    #FINISH TESTING
    # SAVE THIS AS AN EXAMPLE AND AN ACTUAL FUNC


    file_path = "Classifications_from_Glossary_Terms.xlsx"
    classification_info_sheet_name = "TERM_INFO"
    classifications_dict = process_classifications_sheet(file_path, classification_info_sheet_name)
    for c in classifications_dict:
        classification_name = c["classification_name"]
        glossary_term_name = c["glossary_term"]
        print(classification_name)
        result = associate_classification_and_glossary_term(classification_name, glossary_term_name)
        print(result)

    """   



if __name__ == '__main__':
    main()
