##! /usr/bin/env python3


# Imports
# ---------------

import json
import os
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient, AtlasEntity, AtlasProcess
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.core.util import GuidTracker
from sqllineage.runner import LineageRunner
from pathlib import Path


# Functions
# ---------------

def dylan_column_mapping():
    '''
    Need to test
    '''

    # Get your service principal client id, tenant id, and client secret
    # Be sure to store these securely and avoid committing them to version control
    client_id = getpass("Enter your client id: ")
    client_secret = getpass("Enter your client secret: ")
    tenant_id = getpass("Enter your tenant id: ")
    catalog_name = getpass("Enter your catalog name: ")

    # Create the OAuth object to be used in the client.
    oauth = ServicePrincipalAuthentication(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Make the client.
    client = PurviewClient(
        account_name=catalog_name,
        authentication=oauth
    )
    
    # Your SQL query
    sql_query = "SELECT column1, column2 FROM table1 JOIN table2 ON table1.id = table2.id;"

    # Parse the SQL query
    tables_columns = None
    # tables_columns = parse_sql(sql_query)

    # Create the entities and column mapping
    entities = []
    column_mapping = []
    for table, columns in tables_columns.items():
        entity = AtlasEntity(
            name=table,
            typeName="hive_table",
            qualifiedName=f"pyapacheatlas://{table}",
            guid=CLIENT.get_guid()
        )
        entities.append(entity)
        
        for column in columns:
            column_mapping.append(
                {"ColumnMapping": [{"Source": "*", "Sink": column}],
                "DatasetMapping": {"Source": "*", "Sink": entity.qualifiedName}
                }
            )

    # Create the process entity with the column mapping
    process_entity = AtlasProcess(
        name="my_process",
        typeName="Process",
        qualified_name="my_process",
        guid=client.get_guid(),
        attributes={"columnMapping": column_mapping},
        inputs=[{"guid": entity.guid, "typeName": "hive_table"} for entity in entities],
        outputs=[]
    )

    # Upload the entities and the process entity to Atlas
    client.upload_entities([*entities, process_entity])


def extract_column_lineage(sql_file_path: str):
    """
    Need to test
    """
    # Read the SQL file and store its contents as a string
    with open(sql_file_path, 'r') as file:
        sql_string = file.read()

    # Create an instance of LineageRunner
    lineage = LineageRunner(sql_string)
    column_lineage = lineage.get_column_lineage()

    # Get the column lineage
    column_lineage = lineage.get_column_lineage()

    return column_lineage

# Main Function
# ---------------
def main():
    print()


if __name__ == "__main__":
    """
    This sample demonstrates using the columnMapping feature of Azure Purview.
    You will create a process with two inputs and one output. From there you
    will create a valid column mapping JSON object that will display column
    level lineage in the Purview UI.
    """
    oauth = ServicePrincipalAuthentication(
        tenant_id=os.environ.get("TENANT_ID", ""),
        client_id=os.environ.get("CLIENT_ID", ""),
        client_secret=os.environ.get("CLIENT_SECRET", "")
    )
    client = PurviewClient(
        account_name=os.environ.get("PURVIEW_NAME", ""),
        authentication=oauth
    )

    # We need a custom process entity type that contains the definition for
    # a columnMapping attribute.
    procType = EntityTypeDef(
        "ProcessWithColumnMapping",
        superTypes=["Process"],
        attributeDefs = [
            AtlasAttributeDef("columnMapping")
        ]
    )

    # Upload the type definition
    type_results = client.upload_typedefs(entityDefs=[procType], force_update=True)
    print(json.dumps(type_results,indent=2))

    # Set up a guid tracker to make it easier to generate negative guids
    gt = GuidTracker()

    # Now we can create the entities, we will have two inputs and one output
    colMapInput01 = AtlasEntity(
        "Input for Column Mapping",
        "hive_table",
        "pyapacheatlas://colMapInput01",
        guid=gt.get_guid()
    )
    colMapInput02 = AtlasEntity(
        "Second Input for Column Mapping",
        "hive_table",
        "pyapacheatlas://colMapInput02",
        guid=gt.get_guid()
    )
    colMapOutput01 = AtlasEntity(
        "Output for Column Mapping",
        "hive_table",
        "pyapacheatlas://colMapOutput01",
        guid=gt.get_guid()
    )
    
    # Now we can define the column mapping object that will be 'stringified'
    # and given to our process entity
    column_mapping = [
        # This object defines the column lineage between input01 and output01
        {"ColumnMapping": [
            {"Source": "In01Address", "Sink": "Out01Address"},
            {"Source": "In01Customer", "Sink": "Out01Customer"}],
            "DatasetMapping": {
            "Source": colMapInput01.qualifiedName, "Sink": colMapOutput01.qualifiedName}
         },
        # This object defines the column lineage between input02 and output01
        {"ColumnMapping": [
            {"Source": " In02AnnualSales", "Sink": "Out01AnnualSales"},
            {"Source": " In02PostalCode", "Sink": "Out01Address"}],
            "DatasetMapping": {"Source": colMapInput02.qualifiedName, "Sink": colMapOutput01.qualifiedName}
         },
         # This object demonstrates a "special case" of defining fields for one
         # table. The Source is an asterisk for both column mapping and dataset
         # mapping. This is most commonly used to represent "This Sink field is
         # made up of many inputs across all the tables involved in lineage".
         {"ColumnMapping": [
            {"Source": "*", "Sink": "Out01UniqueField3"},
            {"Source": "*", "Sink": "Out01UniqueField4"}],
            "DatasetMapping": {"Source":"*","Sink": colMapOutput01.qualifiedName}
         },
         # This is another example of the above special case for an input object
         {"ColumnMapping": [
            {"Source": "*", "Sink": "In01UniqueField"},
            {"Source": "*", "Sink": "In01UniqueField2"}],
            "DatasetMapping": {"Source": "*", "Sink": colMapInput01.qualifiedName}
         }
    ]

    # Create the process with the stringified column mapping json.
    process = AtlasProcess(
        name="test process",
        typeName="ProcessWithColumnMapping",
        qualified_name="pyapacheatlas://colMapOutputProcessDemo",
        inputs=[colMapInput01, colMapInput02],
        outputs=[colMapOutput01],
        guid=gt.get_guid(),
        attributes={"columnMapping": json.dumps(column_mapping)}
    )

    results = client.upload_entities(
        [process, colMapInput01, colMapInput02, colMapOutput01]
    )

    print(json.dumps(results, indent=2))
    sink_guid = results["guidAssignments"][str(colMapOutput01.guid)]
    print(f"Search for \"{colMapOutput01.name}\" or use the guid {sink_guid} to look up the sink table.")
