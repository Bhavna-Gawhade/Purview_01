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
from utils import get_credentials, create_purview_client


# Import Packages
# ---------------
from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
import json
import datetime
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def generate_s4():
    # Create a Tabular Schema entity
    timestamp = datetime.datetime.now().isoformat()
    ts = AtlasEntity(
        name="S4_tabular_schema",
        typeName="tabular_schema",
        qualified_name="pyapache://s4_tabular_schema/" + timestamp
    )

    # Create a Column entity that references your tabular schema
    timestamp = datetime.datetime.now().isoformat()
    col01 = AtlasEntity(
        name="MaterialNumber",
        typeName="column",
        qualified_name="pyapche://s4_sku/" + timestamp,
        attributes={
            "type":"testing material number",
            "description": "Material Number"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col02 = AtlasEntity(
        name="DivisionCode",
        typeName="column",
        qualified_name="pyapche://s4_division/" + timestamp,
        attributes={
            "type":"testing division code",
            "description": "division code"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col03 = AtlasEntity(
        name="Site",
        typeName="column",
        qualified_name="pyapche://s4_plant/" + timestamp,
        attributes={
            "type":"testing site",
            "description": "site"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col04 = AtlasEntity(
        name="ColorBefore",
        typeName="column",
        qualified_name="pyapche://s4_color_before/" + timestamp,
        attributes={
            "type":"testing color before",
            "description": "color before"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col05 = AtlasEntity(
        name="ColorAfter",
        typeName="column",
        qualified_name="pyapche://s4_color_after/" + timestamp,
        attributes={
            "type":"testing color after",
            "description": "color after"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    # Create a resource set that references the tabular schema
    timestamp = datetime.datetime.now().isoformat()
    rs = AtlasEntity(
        name="S4_demo",
        typeName="azure_datalake_gen2_resource_set",
        qualified_name="pyapache://S4_demo/" + timestamp,
        relationshipAttributes = {
            "tabular_schema": ts.to_json(minimum=True)
        }
    )

    # Upload entities
    results = CLIENT.upload_entities(
        [rs.to_json(), ts.to_json(), col01.to_json(), col02.to_json(), col03.to_json(), col04.to_json(), col05.to_json()]
    )
    # Print out results to see the guid assignemnts
    print(json.dumps(results, indent=2))



def generate_mdg():
    # Create a Tabular Schema entity
    timestamp = datetime.datetime.now().isoformat()
    ts = AtlasEntity(
        name="MDG_tabular_schema",
        typeName="tabular_schema",
        qualified_name="pyapache://mdg_tabular_schema/" + timestamp
    )

    # Create a Column entity that references your tabular schema
    timestamp = datetime.datetime.now().isoformat()
    col01 = AtlasEntity(
        name="Material",
        typeName="column",
        qualified_name="pyapche://mdg_sku/" + timestamp,
        attributes={
            "type":"testing sku",
            "description": "SKU"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col02 = AtlasEntity(
        name="Division",
        typeName="column",
        qualified_name="pyapche://mdg_division/" + timestamp,
        attributes={
            "type":"testing division",
            "description": "division"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col03 = AtlasEntity(
        name="Plant",
        typeName="column",
        qualified_name="pyapche://mdg_plant/" + timestamp,
        attributes={
            "type":"testing plant",
            "description": "Plant"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col04 = AtlasEntity(
        name="ColorA",
        typeName="column",
        qualified_name="pyapche://mdg_color_a/" + timestamp,
        attributes={
            "type":"testing color a",
            "description": "color a"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col05 = AtlasEntity(
        name="ColorB",
        typeName="column",
        qualified_name="pyapche://mdg_color_b/" + timestamp,
        attributes={
            "type":"testing color b",
            "description": "color b"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    # Create a resource set that references the tabular schema
    timestamp = datetime.datetime.now().isoformat()
    rs = AtlasEntity(
        name="MDG_demo",
        typeName="azure_datalake_gen2_resource_set",
        qualified_name="pyapache://MDG_demo/" + timestamp,
        relationshipAttributes = {
            "tabular_schema": ts.to_json(minimum=True)
        }
    )

    # Upload entities
    results = CLIENT.upload_entities(
        [rs.to_json(), ts.to_json(), col01.to_json(), col02.to_json(), col03.to_json(), col04.to_json(), col05.to_json()]
    )
    # Print out results to see the guid assignemnts
    print(json.dumps(results, indent=2))


def generate_plm():
    # Create a Tabular Schema entity
    timestamp = datetime.datetime.now().isoformat()
    ts = AtlasEntity(
        name="PLM_tabular_schema",
        typeName="tabular_schema",
        qualified_name="pyapache://plm_tabular_schema/" + timestamp
    )

    # Create a Column entity that references your tabular schema
    timestamp = datetime.datetime.now().isoformat()
    col01 = AtlasEntity(
        name="SKU",
        typeName="column",
        qualified_name="pyapche://plm_sku/" + timestamp,
        attributes={
            "type":"testing sku",
            "description": "SKU"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col02 = AtlasEntity(
        name="DIV",
        typeName="column",
        qualified_name="pyapche://plm_division/" + timestamp,
        attributes={
            "type":"testing division",
            "description": "division"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    timestamp = datetime.datetime.now().isoformat()
    col03 = AtlasEntity(
        name="Plant",
        typeName="column",
        qualified_name="pyapche://plm_plant/" + timestamp,
        attributes={
            "type":"testing plant",
            "description": "Plant"
        },
        relationshipAttributes = {
            "composeSchema": ts.to_json(minimum=True)
        }
    )

    # Create a resource set that references the tabular schema
    timestamp = datetime.datetime.now().isoformat()
    rs = AtlasEntity(
        name="PLM_demo",
        typeName="azure_datalake_gen2_resource_set",
        qualified_name="pyapache://PLM_demo/" + timestamp,
        relationshipAttributes = {
            "tabular_schema": ts.to_json(minimum=True)
        }
    )

    # Upload entities
    results = CLIENT.upload_entities(
        [rs.to_json(), ts.to_json(), col01.to_json(), col02.to_json(), col03.to_json()]
    )
    # Print out results to see the guid assignemnts
    print(json.dumps(results, indent=2))


def create_column_entity(tabular_schema, qual_name_header, column_name, type):
    col = AtlasEntity(
        name = column_name,
        typeName = "column",
        qualified_name = qual_name_header + column_name + "/",
        attributes = {
            "type": type
        },
        relationshipAttributes = {
            "composeSchema": tabular_schema.to_json(minimum=True)
        }
    )
    return col


def create_all_column_entities(tabular_schema, qual_name_header, columns_dict):
    all_cols = []
    for key, value in columns_dict.items():
        column_name = key
        type = value
        col = create_column_entity(tabular_schema, qual_name_header, column_name, type)
        all_cols.append(col)
    return all_cols


def generate_entity(name, typename, system_name, columns_dict):
    # Create a Tabular Schema entity
    ts = AtlasEntity(
        name = name + "_tabular_schema",
        typeName = "tabular_schema",
        qualified_name = "pyapache://" + system_name + "/" + name + "_tabular_schema/"
    )

    qual_name_header = "pyapache://" + system_name + "/" + name + "_tabular_schema/"
    all_cols = create_all_column_entities(ts, qual_name_header, columns_dict)

    # Create a resource set that references the tabular schema
    rs = AtlasEntity(
        name = name,
        typeName = typename,
        qualified_name = "pyapache://" + system_name + "/" + name + "/",
        relationshipAttributes = {
            "tabular_schema": ts.to_json(minimum=True)
        }
    )

    # Upload entities
    entities = [rs.to_json(), ts.to_json()] + all_cols
    results = CLIENT.upload_entities(entities)
    # Print out results to see the guid assignemnts
    print(json.dumps(results, indent=2))

