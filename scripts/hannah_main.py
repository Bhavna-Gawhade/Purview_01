##! /usr/bin/env python3


# Import Functions
# ---------------

from modules import entity
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *

from modules.lineage.cube_lineage import *
from modules.lineage.databricks_lineage import *
from modules.lineage.data_lake_lineage import *
from modules.lineage.data_warehouse_internal_lineage import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.oracle_server_lineage import *
from modules.lineage.pkms_lineage import *
from modules.lineage.powerbi_sql_query_lineage import *
from modules.lineage.powerbi_tabular_model_lineage import *
from modules.lineage.sap_hana_internal_lineage import *
from modules.lineage.shared_lineage_functions import *
from modules.lineage.sharepoint_lineage import *
from modules.lineage.sql_server_lineage import *

from modules.glossary_propagation.shared_glossary_functions import *
from modules.glossary_propagation.sap_hana_glossary_propagation import *
from modules.glossary_propagation.sap_s4hana_glossary_propagation import *
from modules.glossary_propagation.datalake_glossary_propagation import *
from modules.glossary_propagation.sql_dw_glossary_propagation import *
from modules.entity import *
from modules.collection.collection_shared_functions import *
from modules.collection.sap_s4hana_collection_sorting import *
from modules.collection.azure_dw_collection_sorting import *
from utils import get_credentials, create_purview_client
from pyapacheatlas.core.util import GuidTracker

from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


# Import Packages
# ---------------

from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory, AtlasRelationshipAttributeDef
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
import json
from datetime import datetime
import re
import time
import sys
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


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

def parse_dsp_json_of_table():
    print()
    path_to_file = "RL_FIN_FIGL.json"

    with open(path_to_file, 'r') as json_file:
        json_dict = json.load(json_file)

    table_name =""
    for key in json_dict["definitions"]:
        table_name = key
        break

    table_qualified_name = "sap_hana://86c39b57-6b4c-4172-a3ac-68fa3b408270.hana.prod-us10.hanacloud.ondemand.com/databases/H00/" + "tables/" + table_name
    guid_counter = -1002
    guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
    table_guid = guid_tracker.get_guid()
    table = AtlasEntity(table_name, "sap_hana_table", table_qualified_name, table_guid)

    elements = json_dict["definitions"][table_name]["elements"]
    columns_to_add = []
    for key in elements:
        column_name = key
        column_description = elements[column_name]["@EndUserText.label"]
        column_qualified_name = table_qualified_name + "#" + column_name
        column_guid = guid_tracker.get_guid()
        column = AtlasEntity(column_name, "sap_hana_table_column", column_qualified_name, column_guid, attributes={"type": "str", "userDescription": column_description})
        column.addRelationship(table = table)
        columns_to_add.append(column)

    entities_to_upload = [table] + columns_to_add
    assignments = CLIENT.upload_entities(entities_to_upload)
    print(assignments)


def extract_prod_dsp_td_stg_views(client, dsp_prod_qual_path_header, entity_type):
    #dsp_prod_td_stg_qual_path_header = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/views/"
    browse_result = client.discovery.browse(entityType=entity_type)
    # utilize offset to skip the first results, until you reach the count number
    # result of browse is a dict of @search.count and value
    
    # the "value" gives results in increments of 100
    total_search_count = browse_result.get("@search.count")
    count = 0
    names_of_views = []
    while count < total_search_count:
        browse_result = client.discovery.browse(entityType = entity_type, offset = count)
        entities = browse_result.get("value")
        count += len(entities)
        
        for value_dict in entities:
            if dsp_prod_qual_path_header in value_dict.get("qualifiedName"):
                print(value_dict.get("displayText")) 
                names_of_views.append(value_dict.get("displayText"))
    return names_of_views



def datalake_get_curated_asset(input_file):
    with open(input_file, 'r') as file:
        sql_query = file.read()
        split_sql_query = sql_query.split()
        for i in range(len(split_sql_query)):
            sql_str = split_sql_query[i]
            list_of_keywords = ["into", "create"]
            if sql_str.lower() in list_of_keywords and i != len(split_sql_query) - 1:
                # replace the periods with slashes for searching them as qualified paths
                target = split_sql_query[i + 1].replace(".", "/").replace("_", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                return target

        print("No targets for this view.")
        sys.exit(0)


def datalake_get_stage_asset(input_file):
    with open(input_file, 'r') as file:
        sources = []
        sql_query = file.read()
        split_sql_query = sql_query.split()
        for i in range(len(split_sql_query)):
            sql_str = split_sql_query[i]
            list_of_keywords = ["using", "from", "join"]
            if sql_str.lower() in list_of_keywords and i != len(split_sql_query) - 1:
                # replace the periods with slashes for searching them as qualified paths
                source = split_sql_query[i + 1].replace(".", "/").replace("_", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                if i != len(split_sql_query):
                    if split_sql_query[i + 2] == "SRC":
                        sources.append(source)

        sources = list(set(sources)) # remove duplicates
        sources = [s for s in sources if '/' in s] # removes empty strings and only allows paths
        if len(sources) == 0:
            print("No sources for this view.")
            sys.exit(0)

        return sources
    

def get_inventory_datalake_stage_qualified_name(partial_source_names):
    for name in partial_source_names:
        split_name = name.split("/")
        if len(split_name) != 3:
            print("Not provided all details of stage Ingest source. Verify stage asset name in the stage_Ingest_to_curated_Ingest.sql file.")
        
        source_qualified_name = "https://hbipd01analyticsdls.dfs.core.windows.net/" + split_name[0] + "/Inventory/US/Manual/" + split_name[1] + "/" + split_name[2] + "/{SparkPartitions}"
        print(source_qualified_name)
        print()
        raise Exception
    

def get_target_partial_qual_name(asset_name):
    process_payloads_directory = "BIDW/ProcessPayloads/Curated/"
    if os.path.exists(process_payloads_directory):
        items = os.listdir(process_payloads_directory)
        
        # Filter out only the directories
        folders = [item for item in items if os.path.isdir(os.path.join(process_payloads_directory, item))]
        folder_name = ""
        prod_header = "https://hbipd01analyticsdls.dfs.core.windows.net"

        for folder in folders:
            print("Folder name:", folder)
            folder_path = os.path.join(process_payloads_directory, folder)  # Full path to the subfolder
            files = os.listdir(folder_path)


            # Iterate through the files and capture their names
            seeking = asset_name + ".json"
            for file in files:
                if seeking == file:
                    file_path = os.path.join(folder_path, file)  # Full path to the subfolder

                    folder_name = folder
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        path_to_ingest = data["configurationPayload"]["dataPayload"][0]["dataConfig"]["path"]
                        qual_name_for_ingest = prod_header + path_to_ingest.replace("/mnt", "")
                        print(qual_name_for_ingest)
                        print("\n\n")
                        raise Exception


        raise Exception




def datalake_inventory_stage_ingest_to_curated_ingest():
    path_to_file_with_this_source = ""
    what_we_have_source = "stage.WinningPortfolioSKUList_ingest"
    what_we_need_source = "https://hbipd01analyticsdls.dfs.core.windows.net/stage/Inventory/US/Manual/WinningPortfolioSKUList/Ingest/{SparkPartitions}"


    # iterate through every file in curated and fill in this path
    # pull the source (stage) and target (curated)
    stage_to_curated_directory = "BIDW/Databricks/01/Workflows/Pipelines/Curated/"
    if os.path.exists(stage_to_curated_directory):
        items = os.listdir(stage_to_curated_directory)
        
        # Filter out only the directories
        folders = [item for item in items if os.path.isdir(os.path.join(stage_to_curated_directory, item))]
        for folder in folders:
            if folder == "DimFlatBOM": # HARDCODING
                print("Folder name:", folder)
                file_path = stage_to_curated_directory + folder + "/dependencies/stage_Ingest_to_curated_Ingest.sql"
                
                try:
                    partial_source_names = datalake_get_stage_asset(file_path)
                    partial_target_name = datalake_get_curated_asset(file_path)
                    asset_name = partial_target_name.split("/")[1]
                    print(asset_name)

                    target_partial_qual_name = get_target_partial_qual_name(asset_name)
                    #source_qualified_name = get_inventory_datalake_stage_qualified_name(partial_source_names)

                except:
                    print("Error with " + file_path)

                raise Exception
    else:
        print("The specified path does not exist.")
    
    

    #input_file = "BIDW/Databricks/01/Workflows/Pipelines/Curated/DimWinningPortfolioSkuList/dependencies/stage_Ingest_to_curated_Ingest.sql"
    # will give back something like ["stage/WinningPortfolioSKUList/Ingest"]
    partial_source_names = datalake_get_stage_asset(input_file)
    source_qualified_name = get_inventory_datalake_stage_qualified_name(partial_source_names)


    # iterate through the process payloads until file name found
    # save that sub-directory
    # need to then pull the curated process payload
    # load the process payload json into a dict to extract
    "/mnt/curated/Inventory/US/Manual/DimWinningPortfolioSkuList/Ingest/"
    # remove /mnt, and use this to search, but add header of htt.... first
    

    # then pull entities for both qual names and create lineage


    # then use process payload code to pull this asset again

    what_we_have_target = "curated.DimWinningPortfolioSkuList_Ingest"
    what_we_need_target = "https://hbipd01analyticsdls.dfs.core.windows.net/curated/Inventory/US/Manual/DimWinningPortfolioSkuList/Ingest/{Division}/{SparkPartitions}"



def unassign_then_delete_glossary_terms(client):
    glossary  = client.glossary.get_glossaries(limit = 1)
    #print(glossary)
    terms = glossary[0].get("terms")
    count = 0
    for term in terms:
        if term.get("displayText") != "Material Number" and term.get("displayText") != "Plant" and term.get("displayText") != "Profit Center":
            count += 1
            print("Term: " + term.get("displayText") + ", Count: " + str(count))
            pulled = client.glossary.get_termAssignedEntities(term.get("termGuid"))
            num_to_unassign = len(pulled)
            if num_to_unassign > 0:
                unassign_result = client.glossary.delete_assignedTerm(entities = pulled, termGuid = term.get("termGuid"))
                print(unassign_result)
                print("Unassigned " + term.get("displayText") + " from " + str(num_to_unassign) + " entities")

                
            else:
                print("Unassigned " + term.get("displayText") + " from 0 entities")
            
            delete_term_result = client.glossary.delete_term(term.get("termGuid"))
            print(delete_term_result)
            print("Deleted term " + term.get("displayText"))
            print("\n\n")
        """else:
            pulled = client.glossary.get_termAssignedEntities(term.get("termGuid"))
            num_pulled = len(pulled)
            print("Here " + str(num_pulled))
            this_count = 0
            for pull in pulled:
                print("\n\n")
                print(pull)
                if "guid" in pull and "relationshipGuid" in pull:
                    try:
                        this_count += 1
                        unassign_result = client.glossary.delete_assignedTerm(entities = pull, termGuid = term.get("termGuid"))
                        print("Unassigned " + term.get("displayText") + " from " + str(this_count) + " / " + str(num_pulled))
                    except:
                        print("didn't work")

            delete_term_result = client.glossary.delete_term(term.get("termGuid"))
            print(delete_term_result)
            print("Deleted term " + term.get("displayText"))
            print("\n\n")"""

# Main Function
# ---------------

def main():


    """sharepoint_entity_name = "Control Table ASIN Distribution."
    actual_sharepoint_link = "https://hanes.sharepoint.com/:x:/r/sites/GrowthTeamSupport/_layouts/15/Doc.aspx?sourcedoc=%7B124ACCA7-B22B-4B87-A2F8-ADCCC2CF5563%7D&file=Control%20Table%20ASIN%20Distribution..xlsx&wdLOR=c2860C007-B39E-422A-8453-942CA6124878&action=default&mobileredirect=true"
    pbi_dataset_qualified_name = "https://app.powerbi.com/groups/8864c31d-1a84-42cb-8ae3-a769271b334f/datasets/d2e8f683-32cb-4647-a7d6-c85f701239a7"
    pbi_short_name = "5114AmazonKPIReporting"
    create_sharepoint_entity_and_build_lineage_to_pbi(prod_client, sharepoint_entity_name, actual_sharepoint_link, pbi_dataset_qualified_name, pbi_short_name)
    """

    # example: sql queries to pbi report - connects dw to pbi
    """source_entities_qualified_paths = ["mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/StL/FactTrafficProducts",
                                       "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/StL/FACTATLASSALES",
                                       "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/StL/FACTATLASSALES"
                                       ]
    target_entity_qualified_path = "https://app.powerbi.com/groups/8864c31d-1a84-42cb-8ae3-a769271b334f/datasets/2493cec8-16b1-4a84-9cd5-665db6977909"
    target_name_without_special_char = "5112ServiceProjections"
    build_powerbi_lineage_from_sql_query(prod_client, source_entities_qualified_paths, target_entity_qualified_path, target_name_without_special_char)
    """

    # example: internal data warehouse lineage for table
    # RUN THIS AGAIN - STILL NEED TO DEBUG FOR 51.12 LINEAGE
    table_file_name = "dbo.usp_Facility_SAP_HBI_DW_DLY_FACILITY_SAP.sql"
    #prod_parse_data_warehouse_table_internal_lineage(prod_client, table_file_name)

    """databricks_qualified_name = "default.sbx_retail_sn_osa_rpt@adb-7365464391743055.15.azuredatabricks.net"
    pbi_qualified_name = "https://app.powerbi.com/groups/05ed660c-fa68-47df-ab91-fbc24cff51de/datasets/ce2974e2-2378-4223-9c11-c81db83d3802"
    build_lineage_from_databricks_to_pbi(prod_client, databricks_qualified_name, pbi_qualified_name)
    """


    """stage_guid = "05d7ba22-2c90-47f6-8492-466dd65188e7"
    curated_guid = "1922b826-f907-40a2-b198-d0e014a491f0"
    build_lineage_from_data_lake_stage_to_curated(prod_client, stage_guid, curated_guid)
    """

    """stage_guid = "05d7ba22-2c90-47f6-8492-466dd65188e7"
    curated_guid = "1922b826-f907-40a2-b198-d0e014a491f0"
    build_lineage_from_data_lake_curated_to_data_warehouse_stage(prod_client, stage_guid, curated_guid)
    """

    pull_data_lake_folder = prod_client.get_entity(guid="f10bccb0-82ca-480a-8ff0-adf6f6f60000")
    print(pull_data_lake_folder["entities"][0])


if __name__ == '__main__':
    main()
