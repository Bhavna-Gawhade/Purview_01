##! /usr/bin/env python3


# Import Packages
# ---------------
import json


# Import Functions
# ---------------
from modules.lineage.external_table_lineage import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.shared_lineage_functions import *
from modules.lineage.stored_procedure_lineage import *

# Constants
# ---------------


# Functions
# ---------------

def example_get_and_add_lineage_for_synapse_stored_procedure():
    sql_file_path = "examples/source_code/DimWinningPortfolioSkuList.sql"
    table_names = extract_source_and_target_from_stored_procedure(sql_file_path)
    qualified_name_header = "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/"
    entity_type_name = "synapse_stored_procedure"
    result = get_and_add_lineage(table_names, [qualified_name_header, qualified_name_header], entity_type_name)
    print(json.dumps(result, indent=2))


def example_get_and_add_lineage_for_synapse_external_table():
    sql_file_path = "examples/source_code/Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL.sql"
    table_names = extract_source_and_target_from_external_table(sql_file_path)
    source_header = "https://hbiqa01analyticsdls.dfs.core.windows.net/singlesourcemerged/"
    target_header = "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/"
    entity_type_name = "synapse_external_table"
    result = get_and_add_lineage(table_names, [source_header, target_header], entity_type_name)
    print(json.dumps(result, indent=2))

def example_get_and_add_lineage_from_payload():
    # Open the JSON file using `with open`
    with open(PROJ_PATH.joinpath('examples/source_code','FactFGInventoryAvailability.json')) as json_file:
        # Load the JSON data
        data = json.load(json_file)

    # Process the payload
    payload = process_payload(data = data)
    print(json.dumps(payload, indent=4))
      
    # Add in admin info
    qualified_name_headers = {
        "ingestion_header": "https://hbiqa01analyticsdls.dfs.core.windows.net",
        "synapse_table_header": "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw"
    }
    entity_type_name = "ingestion_framework"

    # Upload the lineage based off of the payload
    results = upload_lineage_from_payload(payload, qualified_name_headers, entity_type_name)
    for result in results:
        print(json.dumps(result, indent=4))
        print()


# Main Function
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()