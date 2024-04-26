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
from modules.lineage.analysis_services_tabular_model_lineage import *
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
from fuzzywuzzy import fuzz


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


def get_entity_from_qualified_name_old(client, qualified_name):
    """
    Retrieves an entity from the catalog based on the provided qualified name.

    Args:
        qualified_name (str): The qualified name of the entity.

    Returns:
        dict: The entity found based on the qualified name.
    """
    entities_found = client.discovery.search_entities(query=qualified_name)
    entities = []
    for entity in entities_found:
      
    
        # Since the input qualified_name is all lowercase, we cannot do a direct str comparison, we must check length
        # This is to avoid qualified names that have the same beginning and different extensions
        # Allow length to differ by 1 for potential '/' at the end
        if (len(entity["qualifiedName"]) == len(qualified_name)) or (len(entity["qualifiedName"]) == len(qualified_name) + 1):
            entities.append(entity)
            return entities[0]

    return None

# Main Function
# ---------------

def get_all_entities_with_type(client, entity_type):
    """
    Retrieves all entities of a specific type in Purview.

    Parameters:
        client (PurviewClient): The Purview client.
        entity_type (str): The name of the entity type.

    Returns:
        dict: Information about all entities of the specified type.
    """
    list_of_guids = get_guids_of_entities_with_specific_type(client, entity_type)
    #print("Pulled all guids for type: " + entity_type)
    #print("Now pulling the entity details for each guid")

    all_entity_details = []
    count = 0


    for guid in list_of_guids:
        count=count+1
        if count==1000:
            break

        pulled = client.get_entity(guid)
        entity = pulled.get("entities")[0]
        entry = {
            "guid": guid, 
            "entity": entity, # just use the first entry
            "columns": entity.get("relationshipAttributes").get("columns")
        }
        if entity_type == "azure_datalake_gen2_resource_set" and "tabular_schema" in entity.get("relationshipAttributes"):
            resource_set_tabular_schema_guid = entity.get("relationshipAttributes").get("tabular_schema").get("guid")
            entry["columns"] = get_columns_from_datalake(client, resource_set_tabular_schema_guid)
            #print(entry["columns"])
        
    
        all_entity_details.append(entry)

    all_entities_with_type = {
        "entity_type": entity_type,
        "info_pulled_on": datetime.now().strftime("%m/%d/%Y %H:%M"),
        "all_entity_details" : all_entity_details
    }
    return all_entities_with_type


def get_entity_from_qualified_name(client, qualified_name):
    """
    Retrieves an entity from the catalog based on the provided qualified name.

    Args:
        qualified_name (str): The qualified name of the entity.

    Returns:
        dict: The entity found based on the qualified name.
    """

    #get all the matching entities from search client
    entities_found = client.discovery.search_entities(query=qualified_name)

    #initialize an empty entity list
    entity_lst = []
    
    #checking for each entity in the entities received if it matches
    #Fuzzy ratio 100 means an exact match
    #If we get an exact match we pick that, otherwise the next best match

    for entity in entities_found:
       

        entity_dict={'entity_name':'' , 'entity_score':0,'entity_dict':{}}
        entity_dict['entity_name']=entity["qualifiedName"]
        entity_dict['entity_dict']=entity

        fuzz_score=fuzz.ratio(entity["qualifiedName"],qualified_name)

      
        entity_dict['entity_name']=max(entity_dict["entity_score"],fuzz_score)
        entity_lst.append(entity_dict)
        if fuzz_score==100 :
            if  (len(entity["qualifiedName"]) == len(qualified_name)) or (len(entity["qualifiedName"]) == len(qualified_name) + 1):
                return entity

    
    best_score=0
    best_entity_dict={}
    for entity in entity_lst:
        if entity['entity_score']>best_score:
            best_score=entity['entity_score']
            best_entity_dict=entity['entity_dict']

    if best_entity_dict=={}:
        return 'No matching names were found'
    return best_entity_dict


       




def main():
    print(datetime.now())
    #qual_name = "https://hbiqa01analyticsdls.dfs.core.windows.net/curated/Business/US/DimBusiness/"
    #qual_name="pkms://file/STSTYL00/record/ST00RC"
    qual_name="https://hbiqa01analyticsdls.dfs.core.windows.net/curated/Product/US/DimItem/Archive/DivisionGroup=/{SparkPartitions}"
    #entity=get_entity_from_qualified_name_old(qa_client, qual_name)
 
    #entity = get_entity_from_qualified_name(qa_client, qual_name)
    #print(entity)
    
    
    all_entities=get_all_entities_with_type(qa_client, entity_type='powerbi_dataset')


    qualified_names=[]
    
    for entity_detail in all_entities['all_entity_details']:

        qualified_names.append(entity_detail['entity']['attributes']['qualifiedName'])
    

    comparison_dict={
        'qualified_name':[],
        'output_old_func':[],
        'output_new_func':[],
        'old_qualified_name':[],
        'new_qualified_name':[]
        }

    for qual_name in qualified_names:
        comparison_dict['qualified_name'].append(qual_name)
        old_output=get_entity_from_qualified_name_old(qa_client, qual_name)
        new_output=get_entity_from_qualified_name(qa_client, qual_name)
        comparison_dict['output_old_func'].append(old_output)
        comparison_dict['output_new_func'].append(new_output)
        if old_output is not None:
            comparison_dict['old_qualified_name'].append(old_output['qualifiedName'])
        if type(new_output)==dict:
            comparison_dict['new_qualified_name'].append(new_output['qualifiedName'])
        
        
    file = open(file='all_entities_output.json', mode='w')
    file.write(str(comparison_dict))
    file.close()

    df=pd.DataFrame(comparison_dict)
    df.to_csv('Comparison_File2_pbi_dataset.csv')
    print(datetime.now())

    





    
    

    
    




if __name__ == '__main__':
    main()
