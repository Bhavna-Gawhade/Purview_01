##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from modules.entity import *
from modules.glossary_propagation.shared_glossary_functions import *


# Package Imports
# ---------------

import json
import os
import re
import time
from datetime import datetime
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.core.glossary import PurviewGlossaryTerm
from pathlib import Path
import pandas as pd



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
    

# Functions
# ---------------

def qa_glossary_propagation_azure_dw():
   # NOTE: some numbers are hard coded. Currently propagating terms 250-500, despite the file containing 1-500.

    """# PROD ACCOUNT
    REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
    CREDS = get_credentials(cred_type= 'default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
    # pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", client)
    """

    client = qa_client

    input_filename = "qa_pulled_entities.json"
    qa_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        qa_pulled_entities = json.load(json_file)

    # use the new regex sheet, extract the glossary term name and regex 
    file_path = "1_to_500_Glossary_with_Field_Duplicates_at_End_10.2.23.xlsx"
    glossary_terms_sheet = pd.read_excel(file_path)
    glossary_terms_dict = []
    for index, row in glossary_terms_sheet.iterrows():
        x = {
            "name": row["Nick Name"],
            "fields": row["Field"].split(",")
        }
        glossary_terms_dict.append(x)

    directory = 'glossary propagation outputs'
    output_file_path = "1_to_250_qa_sql_dw_glossary_propagation_results"

    sql_dw_table_entities = qa_pulled_entities.get("data_sources").get("azure_sql_dw").get("azure_sql_dw_table").get("all_entity_details")

    with open(output_file_path, 'w') as file:
        file.flush()
        count = 0
        for d in glossary_terms_dict: 
            count += 1

            # NOTE: This just applies terms 250-500 since 1-250 has already been run in non-SAP Prod
            #if count >= 501:
            if count >= 251:
                break
            #elif count > 250 and count < 501:
            elif count > 0 and count < 251:
                name = d.get("name")
                fields = d.get("fields")

                azure_sql_dw_table_result = propagate_glossary_term_by_specific_entity_type_and_return_string(sql_dw_table_entities, client, name, fields, "columns")
                
                elapsed_time = azure_sql_dw_table_result[0]
                matched_strings = azure_sql_dw_table_result[1]
                
                end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
                
                return_str = "Glossary term: " + name + "\nPropagated in PROD on: " + str(end_timestamp) + "\nElapsed Time (seconds): " + str(elapsed_time) + "\nNumber of matches, then applications: " + str(len(matched_strings)) + "\nGlossary Term Number: " + str(count) + "\n"
                print(return_str)

                file.write(str(return_str))

                for match in matched_strings:
                    file.write(str(match) + '\n') 
                file.write('\n\n')

        file.flush()
        file.close()
                   

# Main Processing
# ---------------

def main():
    print()

if __name__ == "__main__":
    main()