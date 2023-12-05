##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *
from pyapacheatlas.core.util import GuidTracker


# Imports
# ---------------

import re
import json
import sys
from pathlib import Path


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
    

# Global
# ---------------


# Functions
# ---------------

# create custom PKMS type
# upload type def to QA and Prod
# create tables in Prod and connect lineage

def build_sharepoint_to_pbi_lineage(client, sharepoint_source, sharepoint_short_name, pbi_target, pbi_short_name, process_type_name):
    qualified_name = "sources:" + sharepoint_short_name + "/targets:" + pbi_short_name + "/process_type:" + process_type_name

    sources = []
    targets = []
    s = AtlasEntity(
        name = sharepoint_source["name"],
        typeName = sharepoint_source["entityType"],
        qualified_name = sharepoint_source["qualifiedName"],
        guid = sharepoint_source["id"]
    )
    sources.append(s)

    t = AtlasEntity(
        name = pbi_target["name"],
        typeName = pbi_target["entityType"],
        qualified_name = pbi_target["qualifiedName"],
        guid = pbi_target["id"]
    )
    targets.append(t)

    process = AtlasProcess(
        name = process_type_name,
        typeName = process_type_name,
        qualified_name = qualified_name,
        inputs = sources,
        outputs = targets
    )

    result  = client.upload_entities(
        batch = targets + sources + [process]
    )

    return result


def create_sharepoint_entity(client, entity_name, entity_qualified_name, actual_sharepoint_link):
    guid_counter = -1002
    guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
    entity_guid = guid_tracker.get_guid()
    entity = AtlasEntity(entity_name, "SharePoint Entity", entity_qualified_name, entity_guid, attributes = {"description": "Link to entity in Sharepoint:\n" + actual_sharepoint_link})

    try:
        assignments = client.upload_entities(entity)
        print("Sharepoint entity created for: " + entity_name + "\n")
        sharepoint_entity_dict = {
            "name": entity_name,
            "entityType": "SharePoint Entity",
            "qualifiedName": entity_qualified_name,
            "id": entity_guid
        }
        return sharepoint_entity_dict

    except:
        print("Error with Sharepoint entity: " + entity_name)


def create_sharepoint_entity_and_build_lineage_to_pbi(client, entity_name, actual_sharepoint_link, pbi_dataset_qualified_name, pbi_short_name):
    sharepoint_short_name = entity_name.replace(" ", "_")
    entity_qualified_name = "sharepoint://hanes.sharepoint.com/" + sharepoint_short_name
    sharepoint_dict = create_sharepoint_entity(client, entity_name, entity_qualified_name, actual_sharepoint_link)
    
    pbi_dataset_dict = get_entity_from_qualified_name_using_type(client, pbi_dataset_qualified_name, "powerbi_dataset")
    build_sharepoint_to_pbi_lineage(client, sharepoint_dict, sharepoint_short_name, pbi_dataset_dict, pbi_short_name, "sharepoint_to_pbi")
    print("Lineage built between " + entity_name + " and " + pbi_short_name)


# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()