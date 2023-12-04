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


def propagate_glossary_terms_across_data_lake_resource_sets(datalake_resource_set_entities, client, glossary_term_name, fields):
    #resource_set_guid = "084dda61-3303-4a93-8e8d-274ff6ab6710" # resource set guid, only those have schemas
    #tabular_schema_guid = "0c770d94-f760-4c44-91a9-bef6f6f60000"
    start_time = time.time()
    matched_strings = []

    for resource_set in datalake_resource_set_entities:
        columns = resource_set.get("columns")
        """if relationshipAttributes != None and "tabular_schema" in relationshipAttributes:
            resource_set_tabular_schema_guid = relationshipAttributes.get("tabular_schema").get("guid")
            tabular_schema_details = client.get_entity(resource_set_tabular_schema_guid).get("entities")[0]
            tabular_schema_columns = tabular_schema_details.get("relationshipAttributes").get("columns")
            """

        if columns != None:
            for column in columns:  
                column_guid = column.get("guid")
                column_name = column.get("displayText")

                if column_name in fields:
                    print(f"Matched string: {column_name}")
                    matched_strings.append(column_name)

                    print("column guid: " + str(column_guid))
                    print("entity guid: " + str(resource_set.get("guid")))

                    # want to only apply IF NOT ATTACHED ALREADY - NEED TO IMPLEMENT TO OPTIMIZE
                    entities = [{"guid": column_guid}, {"guid": resource_set.get("guid")}]
                    applied_result = client.glossary.assignTerm(entities = entities, termName = glossary_term_name)
                    print(applied_result)
                
                    ##### haven't checked below
                    """apply_to_resource_set = True
                    for meanings in resource_set_meanings:
                        if meanings.get("displayText") == matching_value:
                            apply_to_resource_set = False # this means the glossary term is already applied to the resource set

                    if not apply_to_resource_set:
                        entities = [{"guid": resource_set_guid}]
                        applied_to_resource_set = CLIENT.glossary.assignTerm(entities = entities, termName = glossary_term_name)
                        print(applied_to_resource_set)

                    entities = [{"guid": column_guid}]
                    applied_to_column = CLIENT.glossary.assignTerm(entities = entities, termName = glossary_term_name)
                    print(applied_to_column)"""

    end_time = time.time()
    elapsed_time_seconds = round(end_time - start_time)

    #end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
    #return_str = "Glossary term: " + glossary_term_name + "\nPropagated in PROD on: " + str(end_timestamp) + "\nElapsed Time (minutes): " + str(elapsed_time_minutes) + "\nNumber of matches, then applications: " + str(matched_strings)
    
    return [elapsed_time_seconds, matched_strings]


def qa_glossary_propagation_of_datalake():
    # run this fresh on QA if need to re-pull entities
    # pull_qa_entities_from_purview("qa", "hbi-qa01-datamgmt-pview", CLIENT)

    client = qa_client
    # CHANGE BACK __ MODIFIED FOR FIX
    #input_filename = "qa_pulled_entities.json"

    input_filename = "datalake_only_qa_pulled_entities.json"
    qa_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        qa_pulled_entities = json.load(json_file)

    # use the new regex sheet, extract the glossary term name and regex 
    glossary_terms_dict = get_glossary_terms_dict()

    directory = 'glossary propagation outputs'
    output_file_path = "1_to_250_qa_datalake_glossary_propagation_results"
    directory = "glossary_propagation_outputs/datalake_outputs"
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    output_file_path = os.path.join(directory, output_file_path)

    datalake_resource_set_entities = qa_pulled_entities.get("data_sources").get("azure_datalake_gen2").get("azure_datalake_gen2_resource_set").get("all_entity_details")

    with open(output_file_path, 'w') as file:
        file.flush()
        count = 0
        for d in glossary_terms_dict: 
            count += 1

            # NOTE: This just applies terms 250-500 since 1-250 has already been run in non-SAP Prod
            if count >= 251:
                #if count >= 501:
                break
            elif count > -1 and count < 251:
                #elif count > 250 and count < 501:
                name = d.get("name")
                fields = d.get("fields")

                datalake_result = propagate_glossary_terms_across_data_lake_resource_sets(datalake_resource_set_entities, client, name, fields)
                
                elapsed_time = datalake_result[0]
                matched_strings = datalake_result[1]
                
                end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
                
                return_str = "Glossary term: " + name + "\nPropagated in QA on: " + str(end_timestamp) + "\nElapsed Time (seconds): " + str(elapsed_time) + "\nNumber of matches, then applications: " + str(len(matched_strings)) + "\nGlossary Term Number: " + str(count) + "\n"
                print(return_str)

                file.write(str(return_str))

                for match in matched_strings:
                    file.write(str(match) + '\n') 
                file.write('\n\n')

        file.flush()
        file.close()


def prod_glossary_propagation_of_datalake():
    REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
    CREDS = get_credentials(cred_type= 'default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

    # RUN BELOW FOR REFRESHED PULL OF PROD INSTANCESs
    #pull_prod_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", client)

    input_filename = "prod_pulled_entities.json"
    prod_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        prod_pulled_entities = json.load(json_file)

    # use the new regex sheet, extract the glossary term name and regex 
    glossary_terms_dict = get_glossary_terms_dict()

    directory = 'glossary propagation outputs'
    #output_file_path = "251_to_500_prod_datalake_glossary_propagation_results"
    output_file_path = "1_to_250_prod_datalake_glossary_propagation_results"

    directory = "glossary_propagation_outputs/datalake_outputs"
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    output_file_path = os.path.join(directory, output_file_path)

    datalake_resource_set_entities = prod_pulled_entities.get("data_sources").get("azure_datalake_gen2").get("azure_datalake_gen2_resource_set").get("all_entity_details")

    with open(output_file_path, 'w') as file:
        file.flush()
        count = 0
        for d in glossary_terms_dict: 
            count += 1

            # NOTE: This just applies terms 250-500 since 1-250 has already been run in non-SAP Prod
            if count >= 251:
                #if count >= 501:
                break
            elif count > -1 and count < 251:
                #elif count > 250 and count < 501:
                name = d.get("name")
                fields = d.get("fields")

                datalake_result = propagate_glossary_terms_across_data_lake_resource_sets(datalake_resource_set_entities, client, name, fields)
                
                elapsed_time = datalake_result[0]
                matched_strings = datalake_result[1]
                
                end_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
                
                return_str = "Glossary term: " + name + "\nPropagated in Prod on: " + str(end_timestamp) + "\nElapsed Time (seconds): " + str(elapsed_time) + "\nNumber of matches, then applications: " + str(len(matched_strings)) + "\nGlossary Term Number: " + str(count) + "\n"
                print(return_str)

                file.write(str(return_str))

                for match in matched_strings:
                    file.write(str(match) + '\n') 
                file.write('\n\n')

        file.flush()
        file.close()
        

# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 

def main():
    print()

if __name__ == "__main__":
    main()