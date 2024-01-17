##! /usr/bin/env python3

# File Notes
# ---------------
__author__ = "Dylan Smith"
__version__ = "1.0"
__email__ = "itsupport@hanes.com"
__status__ = "Testing"


# Imports
# ---------------
from pathlib import Path
import os
from utils import get_credentials, create_purview_client, save_dict_to_json
from pyapacheatlas.auth import BasicAuthentication, ServicePrincipalAuthentication
from pyapacheatlas.core import AtlasEntity, AtlasProcess, PurviewClient
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader
from typing import List, Union, Dict
import json

# Constants
# ---------------
storage_name = "<name of your Storage Account>"
storage_id = "<id of your Storage Account>"
rg_name = "<name of your resource group>"
rg_location = "<location of your resource group>"
REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent

# Get the purview client
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


LINEAGE_CONNECTIONS = {
    "inputs": [
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/stage/Facility_SAP_HBI_DW_DLY_FACILITY_SAP",
         "type": "azure_sql_dw_table"},
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/Common/FactFGInventoryAvailability",
         "type": "azure_sql_dw_table"},
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/mount/Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL",
         "type": "azure_sql_dw_table"},
        {"name": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/Common/DimWinningPortfolioSkuList",
         "type": "azure_sql_dw_table"},
    ],
    "outputs": [{
        "name": "https://app.powerbi.com/groups/87418287-152f-44c8-931d-7fd6228dda48/datasets/5bf85a38-bac9-4101-afc2-0a9ab0717a1a",
        "type": "powerbi_dataset"
    }]
}

# Functions
# ---------------



def create_lineage(client: PurviewClient, inputs: List[AtlasEntity], outputs: List[AtlasEntity], params: dict, testing: bool = True):
    """
    Create lineage between input and output entities using the provided parameters.

    Args:
        client (PurviewClient): The Purview client instance.
        inputs (List[AtlasEntity]): List of input entities.
        outputs (List[AtlasEntity]): List of output entities.
        params (dict): Dictionary containing the required parameters for creating lineage.
            The mandatory parameters are 'name', 'typeName', and 'qualified_name'.

    Raises:
        AssertionError: If any of the mandatory parameters are missing in the 'params' dictionary.

    Returns:
        None
    """

    # Check if all the mandatory parameters are present
    mandatory_params = ['name', 'typeName', 'qualified_name']
    for mp in mandatory_params:
        assert mp in params.keys(), f"Key '{mp}' is not present in the keys list"

    # Define the process to create the lineage
    prvw_proc = AtlasProcess(inputs=inputs, outputs=outputs, **params)

    # Create all the entities if they exist
    BATCH_CREATE = [prvw_proc]

    results = client.upload_entities(batch=BATCH_CREATE)
    assignments = results["guidAssignments"]
    print(assignments)

    if testing:
        # Wait for user input before removing the lineage
        _ = input(">>>Press enter to continue to remove the proper lineage")

        # Remove all the data for assignments
        client.delete_entity(guid=[v for v in assignments.values()])

def process_payload(data: dict) -> Dict[str, List[Dict[str, str]]]:
    """
    Process the JSON payload and extract the source, target, and process payloads.

    Args:
        json_string (str): The JSON payload string.

    Returns:
        Dict[str, List[Dict[str, str]]]: A dictionary containing the source, target, and process payloads.
    """

    # Extract data payloads and process payloads
    data_payloads = data['configurationPayload']['dataPayload']
    process_payloads = data['configurationPayload']['processPayload']

    # Process and extract source and target payloads
    source_payloads = []
    target_payloads = []
    process_info_list = []

    # Process and extract process payloads
    for payload in process_payloads:
        label = payload['label']
        process_config = payload['processConfig']

        # Split label into source and target
        source, target = label.split(' -> ')

        # Add in process to ensure "Curated" matches to "Curated Ingest" in the data payloads
        if target == 'Curated':
            target = "Curated Ingest"
        
        if source == 'Curated':
            source = "Curated Ingest"

        process_info = {
            'processSystem': payload['processSystem'],
            'processType': payload['processType'],
            'label': payload['label'],
            'source': source,
            'target': target,
        }

        # Get the databricks specific information
        if payload['processSystem'] == 'databricks':
            process_info['notebookPath'] = process_config['notebookPath']
            process_info['jobComplexity'] = process_config['linkedService']['jobComplexity']
            process_info['jobSize'] = process_config['linkedService']['jobSize']
        
        process_info_list.append(process_info)

    # Iterate over the data payloads to get the proper objects out
    for payload in data_payloads:

        # Get the label from the payload and extract the true source to link it to the payload
        label = payload['label']
        payload_label = payload['label'].replace(' Source','').replace(' Sink','')
        dataSystem = payload['dataSystem']

        info = {
            'label': label,
            'dataSystem': dataSystem
        }  

        # Pull out the keys
        if 'dataSource' in payload.keys():
            info['dataSource'] = payload['dataSource']

        # Pull out the data config if it is present
        if 'dataConfig' in payload.keys():
            data_config = payload['dataConfig']

            # Include 'path' if present in dataConfig as well as 'synapseTable' and 'mergeProcedure'
            for attr in ['path','synapseTable','mergeProcedure']:
                if attr in data_config:
                    info[attr] = data_config[attr]

        # If data extractor is dataFactory, compile the full path of the data
        if payload['dataSystem'] == 'dataFactory':
            info['path'] = f"/{payload['config']['container']}/{payload['config']['directory']}"

        # Include Extract the sink
        if 'Sink' in label:
            target_payloads.append(info)

        # Add to the source payloads list if the payload is a 'Source'
        elif 'Source' in label:
            source_payloads.append(info)

        # Iterate over all processes and find where the object is a source or sink
        for proc in process_info_list:
            if payload_label == proc['source'] and dataSystem == proc['processSystem']:
                proc['sourceDataPayload'] = info 
            elif payload_label == proc['target'] and dataSystem == proc['processSystem']:
                proc['targetDataPayload'] = info
            
    # Create dictionary with source, target, and process payloads
    result = {
        "source": source_payloads,
        "target": target_payloads,
        "process": process_info_list
    }

    return result

def get_guid_from_fully_qualified_path(fully_qual_path: str, save_as_file: bool) -> Union[str, None]:
    """
    Get the GUID of an entity based on its fully qualified path.

    Args:
        fully_qual_path (str): The fully qualified path of the entity.
        save_as_file (bool): Flag indicating whether to save the entity as a JSON file.

    Returns:
        Union[str, None]: The GUID of the entity. None if no entity is found.

    Raises:
        Exception: If more than one entity is found with the given fully qualified path.
    """

    # Get the entities from the object
    entities_found = CLIENT.discovery.search_entities(query=fully_qual_path)
    obj_name = fully_qual_path.split('/')[-1]

    # Extract all entities that are found by the search catalog
    entities = []
    for entity in entities_found:
        entities.append(entity)

    # Ensure that the list has a length of 1, if not it has found multiple entities.
    if len(entities) > 1:
        raise Exception(f'Found more than one entity: {entities}')

    # Get the GUID
    guid = entities[0]['id']

    if save_as_file:
        save_dict_to_json(data=entity,
                          path=PROJ_PATH.joinpath('outputs', 'lineage_testing'),
                          filename=f"{obj_name}.json")

    print(f'Found the GUID: {guid} for object {fully_qual_path}')

    return guid

def main(payload: dict):
    """
    This function tries to get the report from Amazon's Selling Partner API and a GetReportResponse object is created from the report payload. The function returns a dictionary of the GetReportResponse object. 
    

    Args:
        reportResponse (dict): The report response to pass to the API monitor api

    Returns:
        dict: The report response from the object from the API
    """
    ### Testing
    
    # Get all type definitions from the account
    if payload['download'] == 'typedefs':
        results = CLIENT.get_all_typedefs()

    if payload['testing'] == 'ingestion_parser':

        # Open the JSON file using `with open`
        with open(PROJ_PATH.joinpath('scripts','GsxAPIDownloadProducts.json')) as json_file:
            # Load the JSON data
            data = json.load(json_file)

        # Process the Payload
        payloads = process_payload(data = data)
        print(json.dumps(payloads, indent=4))
    
    if payload['testing'] == 'lineage':

        lineage_params = {
            "typeName": "Process",
            "qualifiedName": "pyapacheatlas://democustomprocess",
            "name": "PowerBI Inventory Dataset Upload"
        }

        # Get the lineage inputs and outputs
        inputs = []
        for objs in LINEAGE_CONNECTIONS["inputs"]:

            entities = CLIENT.get_entity(
                qualifiedName= objs['name'],
                typeName=objs['type']
            )

            for entity in entities.get("entities"):
                print('Adding entity to list')
                inputs.append(entity)

        outputs = []
        for objs in LINEAGE_CONNECTIONS["outputs"]:

            entities = CLIENT.get_entity(
                qualifiedName= objs['name'],
                typeName=objs['type']
            )

            for entity in entities.get("entities"):
                print('Adding entity to list')
                outputs.append(entity)

        create_lineage(inputs = inputs, outputs = outputs, params = lineage_params)
    
    if payload['testing'] == 'entity':
        qual_name = 'mssql://hbidevsqldbsrv.database.windows.net'

        #while True:
        entities_found = CLIENT.discovery.search_entities(query = qual_name)
        datalake_paths = ['azure_datalake_gen2_resource_set','azure_datalake_gen2_path','azure_datalake_gen2_filesystem','azure_datalake_gen2_service','azure_storage_account']
        blob = ['azure_blob_path','azure_blob_service','azure_blob_container','azure_storage_account']
        dw_objs = ['azure_sql_dw_table','azure_sql_dw','azure_sql_dw_schema']
        dbs = ['mssql_table','mssql_instance','mssql_db','mssql_schema']
        az_dbs = ['azure_sql_db']
        for entity in entities_found:
            if entity['entityType'] not in az_dbs:
                print(f'Found a random entity type: {entity["entityType"]}')
                break
            else:
                print(entity['entityType'])
            
            
            print(entity['qualifiedName'])
            CLIENT.delete_entity(guid=entity['id'])

    
if __name__ == '__main__':

    # Define the payload for testing and dev
    payload = {'download': '',
               'testing': 'ingestion_parser'}
    main(payload= payload)