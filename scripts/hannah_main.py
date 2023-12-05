##! /usr/bin/env python3


# Import Functions
# ---------------

from modules import entity
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.shared_lineage_functions import *
from modules.lineage.powerbi_sql_query_lineage import *
from modules.lineage.powerbi_tabular_model_lineage import *
from modules.lineage.data_warehouse_internal_lineage import *
from modules.lineage.sap_hana_internal_lineage import *
from modules.lineage.sharepoint_lineage import *
from modules.lineage.pkms_lineage import *
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

def create_sap_hana_table_for_dsp():
    print()
    """
    # try pulling the table
    qualified_name = "TESTING_A_QUALIFIED_NAME_TEST"
    entities_found = CLIENT.discovery.search_entities(query=qualified_name)
    entities = []
    for entity in entities_found:
        entities.append(entity)
        break
    print(entities[0])

    print("\n\n\n")
    print(CLIENT.get_entity("8bac6f05-78c3-47f8-a81d-4ef6f6f60000").get("entities")[0])
    """



    """# doing this in QA for testing
    new_sap_hana_table = AtlasEntity(
        name = "TEST CREATE SAP HANA TABLE",
        typeName = "sap_hana_table",
        qualified_name = "TESTING_A_QUALIFIED_NAME_TEST"
        #guid = "123456789123456789" #DO NOT PROVIDE GUid, wont work
    )
    res = CLIENT.upload_entities(batch = new_sap_hana_table)
    print(res)"""

    """new_sap_hana_column = {
                    #"guid": "8f28b97d-3273-4294-81b0-50f6f6f60000",
                    "typeName": "sap_hana_table_column",
                    #"entityStatus": "ACTIVE",
                    "displayText": "TESTING PLEAE COL",
                    "relationshipType": "sap_hana_table_columns",
                    #"relationshipGuid": "2b12490e-945d-4e75-990c-e213bad04982",
                    #"relationshipStatus": "ACTIVE",
                    "relationshipAttributes": {
                        "typeName": "sap_hana_table_columns"
                    }}"""

    """new_relationship_attributes = {
        "table_columns": [new_sap_hana_column]
    }"""

    new_sap_hana_table = AtlasEntity(
        name = "TEST CREATE SAP HANA TABLE",
        typeName = "sap_hana_table",
        qualified_name = "TESTING_A_QUALIFIED_NAME_TEST"
        #guid = "123456789123456789"
        #relationshipAttributes = new_relationship_attributes
    )



    s = AtlasEntity(
        name = "PLEASE LET ME CREATE A COLUMN",
        typeName = "sap_hana_table_column",
        qualified_name = "PLEASE LET ME CREATE A COLUMN FOR SAP HANA"
        #guid = 'ATTE<PTATTEMPT'
    )

   
    t = AtlasEntity(
        name = "TEST CREATE SAP HANA TABLE",
        typeName = "sap_hana_table",
        qualified_name = "TESTING_A_QUALIFIED_NAME_TEST"
        #guid = entity["id"]
    )

    print("HERE????")

    process = AtlasRelationshipAttributeDef(
        name = "TRY_TO_CREATE_SAP_HANA_COLUMN",
        relationshipTypeName = "sap_hana_table_columns",
        qualified_name = "PLEASE_UPLOAD_SAP_HANA_COLUMN",
        inputs = s,
        outputs = t
    )

    print("HERE?")

    result  = CLIENT.upload_entities(
        batch = [s, t, process]
    )
    
    print(result)

    raise Exception


    res = CLIENT.upload_entities(batch = new_sap_hana_table)
    print(res)


def pull_sap_hana_table():
    res = CLIENT.discovery.browse("sap_hana_table")
    print(res)


def try_again_to_create_sap_hana_table_for_dsp():
    print()


    new_sap_hana_table = AtlasEntity(
        name = "TEST 101623 CREATE SAP HANA TABLE",
        typeName = "sap_hana_table",
        qualified_name = "TESTING_A_QUALIFIED_NAME_TEST"
        #guid = "123456789123456789"
        #relationshipAttributes = new_relationship_attributes
    )





    s = AtlasEntity(
        name = "PLEASE LET ME CREATE A COLUMN",
        typeName = "sap_hana_table_field",
        qualified_name = "PLEASE LET ME CREATE A COLUMN FOR SAP HANA"
        #guid = 'ATTE<PTATTEMPT'
        #relationshipAttributes = new_relationship_attributes
    )

   
    t = AtlasEntity(
        name = "TEST 101623 CREATE SAP HANA TABLE",
        typeName = "sap_hana_table",
        qualified_name = "TESTING_A_QUALIFIED_NAME_TEST",
        #guid = entity["id"]
        #relationshipAttributes = s        
        relationshipAttributes = {"columns": ["hi", "hello"]}

    )

    print("HERE????")

    process = AtlasRelationshipAttributeDef(
        name = "TRY_TO_CREATE_SAP_HANA_COLUMN",
        relationshipTypeName = "sap_hana_table_fields",
        qualified_name = "PLEASE_UPLOAD_SAP_HANA_COLUMN",
        inputs = s,
        outputs = t
    )

    print("HERE?")

    result  = CLIENT.upload_entities(
        #batch = [s, t, process]
        #batch = [s, t]
        #batch = [t]
        batch = [process]

    )
    
    print(json.dumps(result))

    

def create_dsp_table_with_excel():
    ec = ExcelConfiguration()
    reader = ExcelReader(ec)

    entities = reader.parse_bulk_entities("path/to/spreadsheet.xlsx")

    results = CLIENT.upload_entities(entities)

    print(json.dumps(results, indent=2))


def pyapache_relationship_walkthrough():
    # Creating the entities that will be used in uploads.
    # One table will be added
    table = AtlasEntity("rel10","sap_hana_table", "tests://rel10", guid="-1")
    # Four columns will be added
    c1 = AtlasEntity("rel10#01", "sap_hana_table_column", "tests://rel10#c", guid="-2", attributes={"type":"str"})
    c2 = AtlasEntity("rel10#02", "sap_hana_table_column", "tests://rel02#c", guid="-3", attributes={"type":"str"})
    c3 = AtlasEntity("rel10#03", "sap_hana_table_column", "tests://rel03#c", guid="-4", attributes={"type":"str"})
    c4 = AtlasEntity("rel10#04", "sap_hana_table_column", "tests://rel04#c", guid="-5", attributes={"type":"str"})

    # Add relationships to the columns from the table overwriting existing columns
    # Good if you want to overwrite existing schema or creating a brand new table
    # and Schema.
    columns_to_add = [ c1, c2, c3 ]
    # Use a list comprehension to convert them into dictionaries when adding a list
    table.addRelationship(columns=[c.to_json(minimum=True) for c in columns_to_add])

    # OR Add a table relationship to a column. This lets you essentially APPEND
    # a column to a table's schema.
    c4.addRelationship(table = table)

    # Upload all of the tables and columns that are referenced.
    assignments = CLIENT.upload_entities([table, c1, c2, c3, c4])["guidAssignments"]
    print(assignments)


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


def get_all_incorrect():
    incorrect = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/tables/MD_STG/views/"
    incorrect = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/tables/TD_STG/views/"

    input_filename = "prod_pulled_entities.json"
    prod_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        prod_pulled_entities = json.load(json_file)
    hana_view_entities = prod_pulled_entities.get("data_sources").get("sap_hana").get("sap_hana_view").get("all_entity_details")

    all_incorrect = []
    incorrect_guids = []
    for e in hana_view_entities:
        if incorrect in e.get("entity").get("attributes").get("qualifiedName"):
            print(e.get("entity").get("attributes").get("qualifiedName"))
            all_incorrect.append(e.get("entity").get("attributes").get("qualifiedName"))
            incorrect_guids.append(e.get("guid"))
            result = prod_client.delete_entity(e.get("guid"))
            print(result)
            print()

    print(len(all_incorrect))
    #result = prod_client.delete_entity(incorrect_guids)
    #print(result)


def delete_all_incorrect_dsp_connections():
    #dsp_prod_td_stg_qual_path_header = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/views/"
    entity_type = "dsp_connection"
    browse_result = prod_client.discovery.browse(entityType=entity_type)

    total_search_count = browse_result.get("@search.count")
    count = 0
    names_of_views = []
    deleted_count = 0
    all_guids = []
    while count < total_search_count:
        browse_result = prod_client.discovery.browse(entityType = entity_type, offset = count)
        entities = browse_result.get("value")
        count += len(entities)
        
        for value_dict in entities:
            if value_dict.get("entityType") == entity_type:
                #result = prod_client.delete_entity(value_dict.get("id"))
                #print(result)
                print()
                all_guids.append(value_dict.get("id"))
                print("okay " + str(deleted_count))
                deleted_count += 1

    error_guids = ["4dc9578d-6347-43c1-bd90-1d4524e365f6", "06ea1a10-8bac-49bf-a7e1-818fe65132d1", "045007da-621e-4f5c-bc48-323a39e6d7df"]
    for guid in all_guids:
        try:
            if guid not in error_guids:
                print(guid)
                result = prod_client.delete_entity(guid)
                print(result)
                print()
        except:
            print("error with guid: " + str(guid))
    print("Deleted " + str(deleted_count))


def get_views_that_should_be_tables():
    input_filename = "prod_pulled_entities.json"
    prod_pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        prod_pulled_entities = json.load(json_file)
    sap_hana_view_details = prod_pulled_entities.get("data_sources").get("sap_hana").get("sap_hana_view").get("all_entity_details")
    #sap_hana_table_details = prod_pulled_entities.get("data_sources").get("sap_hana").get("sap_hana_table").get("all_entity_details")
    
    incorrect = []
    guids = []
    for view in sap_hana_view_details:
        name = view.get("entity").get("attributes").get("name")
        if name.startswith("ZV_") or name.startswith("ZC_") or name.startswith("TA_"):
            print(name)
            incorrect.append(name)
            result = prod_client.delete_entity(view.get("guid"))
            print(result)
    print(len(incorrect))
    

def get_weird_dsp_connections():
    #dsp_prod_td_stg_qual_path_header = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/views/"
    entity_type = "dsp_connection"
    browse_result = prod_client.discovery.browse(entityType=entity_type)

    total_search_count = browse_result.get("@search.count")
    count = 0
    names_of_views = []
    deleted_count = 0
    all_guids = []
    while count < total_search_count:
        browse_result = prod_client.discovery.browse(entityType = entity_type, offset = count)
        entities = browse_result.get("value")
        count += len(entities)
        
        for value_dict in entities:
            if value_dict.get("entityType") == entity_type:
                if "ZV_" in value_dict.get("qualifiedName") or "ZC_" in value_dict.get("qualifiedName") or "TA_" in value_dict.get("qualifiedName"):
                    print() 
                    all_guids.append(value_dict.get("id"))
                    print("okay " + str(deleted_count))
                    deleted_count += 1
                    print()
                    print(value_dict)
                    print()
                    return
                
                
def pull_a_dsp_connection():
    without_guid = "7bc431e7-b9b9-4cd8-9924-c14041cb79a2"
    with_guid = "e7ea8363-9523-4ab1-bc18-dd5a28e4a5fe"
    #result = prod_client.get_relationship(guid)
    result = prod_client.get_entity(with_guid)

    print(result)


def pull_dsp_connections_without_inputs_or_outputs():
    input_filename = "prod_pulled_lineage_connections.json"
    prod_pulled_lineage_connections = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        prod_pulled_lineage_connections = json.load(json_file)

    dsp_connections = prod_pulled_lineage_connections.get("lineage_connections").get("dsp_connection").get("all_entity_details")

    all_incorrect = []
    incorrect_guids = []
    guids_to_delete = []
    for c in dsp_connections:
        inputs = c.get("entity").get("attributes").get("inputs")
        outputs = c.get("entity").get("attributes").get("outputs")

        if outputs == [] or outputs == None or inputs == [] or inputs == None:
            print(c.get("guid"))
            guids_to_delete.append(c.get("guid"))
    print(len(guids_to_delete))

    delete_count = 0
    total_count = len(guids_to_delete)
    for guid in guids_to_delete:
        delete_count += 1
        print("Count: " + str(delete_count) + " / " + str(total_count))
        print("Guid: " + guid)
        result = prod_client.delete_entity(guid)
        print(result)
        print()
        print()
        

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
    print()

    #datalake_to_data_warehouse_lineage_from_payload(file_name)
    #extract_fields_for_which_there_are_not_glossary_terms()

    #pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)
    #prod_glossary_propagation_of_sap_hana()
    #prod_glossary_propagation_of_sap_s4hana()
    #parse_sap_hana_internal_lineage()

    # USE BELOW TO EXTRACT VIEW NAMES OF VIEWS FOR CERTAIN SCHEMA
    """
    dsp_prod_with_schema_qual_path_header = "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/FIN_REP/views/"
    entity_type = "sap_hana_view"
    entities = extract_prod_dsp_td_stg_views(prod_client, dsp_prod_with_schema_qual_path_header, entity_type)
    print(len(entities))
    """

    #parse_sap_hana_internal_lineage()

    #prod_glossary_propagation_of_sap_hana()

    guid = "b3d8cd07-6b6e-480f-8c4e-f9f6f6f60000"
    #result = prod_client.get_entity(guid)
    #print(result)


    # ADDRESS COLUMN DUPLICATES
    # ADDRESS COLUMNs AND DESCRIPTIONS NOT IMPORTED



    #########
    #parse_sap_hana_internal_lineage()
    # R 
    # U
    # N
    # THIS!!!! after gloss prop today
    ############



    #get_all_incorrect()

    #delete_all_incorrect_dsp_connections()
    #pull_lineage_connections_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)

    #get_views_that_should_be_tables()
    
    
    #get_weird_dsp_connections()
    #pull_a_dsp_connection()
    #pull_dsp_connections_without_inputs_or_outputs()

    #print(prod_client.get_entity("830f4fa8-3c1b-4015-b173-9bb17b50d7b9"))

    #file_name = "ProcessPayloads/Curated/Business/DimBusiness.json"
    #datalake_to_data_warehouse_lineage_from_payload(prod_client, file_name)


    #parse_data_warehouse_interplatform_lineage(prod_client, "Inventory.vwDimCurrency.sql")

    #datalake_inventory_stage_ingest_to_curated_ingest()

    #unassign_then_delete_glossary_terms(prod_client)
    #build_powerbi_lineage_from_sql_query(prod_client)
    #prod_parse_data_warehouse_table_internal_lineage(prod_client, "Explore.AmzFactDaily.sql")


    """sharepoint_entity_name = "Control Table ASIN Distribution."
    actual_sharepoint_link = "https://hanes.sharepoint.com/:x:/r/sites/GrowthTeamSupport/_layouts/15/Doc.aspx?sourcedoc=%7B124ACCA7-B22B-4B87-A2F8-ADCCC2CF5563%7D&file=Control%20Table%20ASIN%20Distribution..xlsx&wdLOR=c2860C007-B39E-422A-8453-942CA6124878&action=default&mobileredirect=true"
    pbi_dataset_qualified_name = "https://app.powerbi.com/groups/8864c31d-1a84-42cb-8ae3-a769271b334f/datasets/d2e8f683-32cb-4647-a7d6-c85f701239a7"
    pbi_short_name = "5114AmazonKPIReporting"
    create_sharepoint_entity_and_build_lineage_to_pbi(prod_client, sharepoint_entity_name, actual_sharepoint_link, pbi_dataset_qualified_name, pbi_short_name)
    """

    #pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)
    #pull_entities_from_purview("qa", "hbi-qa01-datamgmt-pview", qa_client)
    #pull_lineage_connections_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)
    #pull_sap_s4hana_columns_of_table("prod", "MARA")
    #pull_sap_s4hana_table_columns_without_glossary_terms("prod", "MARA")


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
    # !
    # RUN THIS AGAIN - STILL NEED TO DEBUG FOR 51.12 LINEAGE
    # !
    # !
    table_file_name = "Explore.KeplerMediaSpend.sql"
    #prod_parse_data_warehouse_table_internal_lineage(prod_client, table_file_name)
    
    # example: internal data warehouse lineage for table
    view_file_name = "dbo.vw_DimCustomerAccount_scv.sql"
    #prod_parse_data_warehouse_view_internal_lineage(prod_client, view_file_name)

    #glossary_propagation_of_sap_hana(prod_client, "prod", "11_15_23_Purview_Glossary_Import_716_Terms.xlsx")
    #glossary_propagation_of_sap_s4hana(prod_client, "prod", "11_15_23_Purview_Glossary_Import_716_Terms.xlsx")
    #pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)

    file_name = "ProcessPayloads/Curated/Business/DimBusiness.json"
    #datalake_to_data_warehouse_lineage_from_payload(prod_client, )


    #parse_pkms_tables_from_excel(qa_client, "PKMS_Metadata.xlsx")
    pkms_file_path = "input_files/pkms_for_pyapacheatlas/STSTYL00_PyApacheAtlas.xlsx"
    #upload_pkms_record_from_excel(qa_client, pkms_file_path)

    pkms_guid = "664a4887-5784-4f1c-9f92-5f5126f938aa"
    #pkms_entity = qa_client.get_entity(pkms_guid).get("entities")[0]
    #print(pkms_entity)

    source_qual = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/mount/Product_Item_Attribute_OAKDWHP1"
    target_qual = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/master/DimAttribute"

    source_entity = get_entity_from_qualified_name(prod_client, source_qual)
    target_entity = get_entity_from_qualified_name(prod_client, target_qual)
    process_type_name = "dw_routine"
    result = add_manual_lineage(prod_client, [source_entity], [target_entity], process_type_name)
    print(result)
    
    #manually_connect_dl_to_dw_via_qualified_names(prod_client, source_qual, target_qual)






if __name__ == '__main__':
    main()
