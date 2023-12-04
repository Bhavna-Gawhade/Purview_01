##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *


# Imports
# ---------------

import re
import sys
from pathlib import Path


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def alternate_parse_load_routine_for_data_warehouse(load_routine_file):
    with open(load_routine_file, 'r') as file:
        sources = []
        sql_query = file.read()
        sql_queries = sql_query.split('GO')
        sources_to_ignore = ["sys/objects"]

        for query in sql_queries:
            keywords = ['from', 'join', 'using', 'exec']
            for keyword in keywords:
                splitted_query = query.strip().replace('\x00', '').replace('\n', ' ').lower().split(keyword)
                for i in range(1, len(splitted_query)):
                    after_keyword = splitted_query[i].strip()
                    split_after_keyword = after_keyword.split()
                    if len(split_after_keyword) > 0:
                        source = split_after_keyword[0].replace(".", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                        if not source.startswith("#") and source not in sources_to_ignore and keyword != "exec":
                            sources.append(source)                        

        return sources
    

def parse_load_routine_for_data_warehouse(load_routine_file):
    with open(load_routine_file, 'r') as file:
        sources = []
        sql_query = file.read()
        split_sql_query = sql_query.split()

        if not any("\x00" in element for element in split_sql_query):
            sources_to_ignore = ["sys/objects"]
            for i in range(len(split_sql_query)):
                sql_str = split_sql_query[i]
                list_of_keywords = ["using", "from", "join"]
                if sql_str.lower() in list_of_keywords and i != len(split_sql_query) - 1:
                    # replace the periods with slashes for searching them as qualified paths
                    source = split_sql_query[i + 1].replace(".", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                    if not source.startswith("#") and source not in sources_to_ignore:
                        sources.append(source)
        
        else:
            sources = alternate_parse_load_routine_for_data_warehouse(load_routine_file)
        
        sources = list(set(sources)) # remove duplicates
        sources = [s for s in sources if '/' in s] # removes empty strings and only allows paths
        if len(sources) == 0:
            print("No stage sources for this table.")
            sys.exit(0)

        return sources



def alternate_parse_view_for_data_warehouse(view_file):
    with open(view_file, 'r') as file:
        sources = []
        sql_query = file.read() 
        sql_queries = sql_query.split('GO')
        sources_to_ignore = ["sys/objects"]

        for query in sql_queries:
            keywords = ['from', 'join', 'using']
            for keyword in keywords:
                splitted_query = query.strip().replace('\x00', '').replace('\n', ' ').lower().split(keyword)
                for i in range(1, len(splitted_query)):
                    after_keyword = splitted_query[i].strip()
                    split_after_keyword = after_keyword.split()
                    if len(split_after_keyword) > 0:
                        source = split_after_keyword[0].replace(".", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                        if not source.startswith("#") and source not in sources_to_ignore:
                            sources.append(source)

        return sources


def parse_view_for_data_warehouse(view_file):
    with open(view_file, 'r') as file:
        sources = []
        sql_query = file.read()
        try: 
            split_sql_query = sql_query.split("")
            for i in range(len(split_sql_query)):
                sql_str = split_sql_query[i]
                list_of_keywords = ["using", "from", "join"]
                if sql_str.lower() in list_of_keywords and i != len(split_sql_query) - 1:
                    # replace the periods with slashes for searching them as qualified paths
                    source = split_sql_query[i + 1].replace(".", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                    sources.append(source)
        except:
            sources = alternate_parse_view_for_data_warehouse(view_file)

        sources = list(set(sources)) # remove duplicates
        sources = [s for s in sources if '/' in s] # removes empty strings and only allows paths
        if len(sources) == 0:
            print("No sources for this view.")
            sys.exit(0)

        print(sources)

        return sources
    

def ORIGINAL_parse_view_for_data_warehouse(view_file):
    with open(view_file, 'r') as file:
        sources = []
        sql_query = file.read()
        
        split_sql_query = sql_query.split("")
        for i in range(len(split_sql_query)):
            sql_str = split_sql_query[i]
            list_of_keywords = ["using", "from", "join"]
            if sql_str.lower() in list_of_keywords and i != len(split_sql_query) - 1:
                # replace the periods with slashes for searching them as qualified paths
                source = split_sql_query[i + 1].replace(".", "/").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(";", "")
                sources.append(source)

        sources = list(set(sources)) # remove duplicates
        sources = [s for s in sources if '/' in s] # removes empty strings and only allows paths
        if len(sources) == 0:
            print("No sources for this view.")
            sys.exit(0)

        return sources

def build_table_to_source_data_warehouse_internal_lineage(client, qualified_name_header, table, source):
    # stage (source) to table 
    source_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + source)
    target_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + table)
    
    if source_entity.get("qualifiedName") != target_entity.get("qualifiedName"):
        result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name = "dw_routine")
        print(result)


def build_stage_to_common_data_warehouse_internal_lineage(client, qualified_name_header, common_source_for_the_view, stage_source_for_common, view_purview_partial_path):
    # stage to common 
    source_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + stage_source_for_common)
    target_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + common_source_for_the_view)
    
    if source_entity.get("qualifiedName") != target_entity.get("qualifiedName"):
        result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name = "dw_routine")
        print(result)
    
    # common to view
    source_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + common_source_for_the_view)
    target_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + view_purview_partial_path)
    if source_entity.get("qualifiedName") != target_entity.get("qualifiedName"):
        result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name = "dw_view_creation")
        print(result)


def prod_parse_data_warehouse_view_internal_lineage(client, view_file_name):
    try:
        qualified_name_header = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/"
        #Example: view_file_name = "Inventory.vwDimMarketingResponsibilityHierarchy.sql"
        view_file_path = "data_warehouse_install/Views/" + view_file_name
        view_purview_partial_path = view_file_name.replace(".sql", "").replace(".", "/")
        common_sources_for_the_view = parse_view_for_data_warehouse(view_file_path)
        print(common_sources_for_the_view)

        for common_source in common_sources_for_the_view:
            print(common_source)
            split_common_source = common_source.split("/")
            load_routine_file_path = "data_warehouse_install/Routines/" + split_common_source[0] + ".Load" + split_common_source[1] + ".sql"
            
            if common_source == "Common/FactSales" or common_source == "common/FactSales": # ERROR IN NAMING SCHEMA FOR THIS TABLE LOAD ROUTINE
                load_routine_file_path = "data_warehouse_install/Routines/Common.LoadFactSalesDaily.sql"
            elif common_source == "Common/DimFlatHierarchalBOM": # ERROR IN NAMING SCHEMA FOR THIS TABLE LOAD ROUTINE
                load_routine_file_path = "data_warehouse_install/Routines/Common.LoadFlatHierarchalBOM.sql"
            elif common_source.lower().startswith("master"):
                split_table = common_source.split("/")
                load_routine_file_path = "data_warehouse_install/Routines/master.load_" + split_table[1] + ".sql"
            elif common_source.lower().startswith("dbo"):
                split_table = common_source.split("/")
                load_routine_file_path = "data_warehouse_install/Routines/dbo.load_" + split_table[1] + ".sql"

            if split_common_source[1].startswith("mvw") or split_common_source[1].startswith("vw"):
                new_view_file_name = split_common_source[0] + "." + split_common_source[1] + ".sql"
                prod_parse_data_warehouse_view_internal_lineage(client, new_view_file_name)
                # still need to connect this to the original view
                source_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + common_source)
                target_entity = get_entity_from_qualified_name_with_specific_client(client, qualified_name_header + view_purview_partial_path)
                if source_entity.get("qualifiedName") != target_entity.get("qualifiedName"):
                    result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name = "dw_view_creation")
                    print(result)
            else:  
                stage_sources_for_common = parse_load_routine_for_data_warehouse(load_routine_file_path)
                for stage_source in stage_sources_for_common:
                    if stage_source != common_source: # prevent loop to itself
                        build_stage_to_common_data_warehouse_internal_lineage(client, qualified_name_header, common_source, stage_source, view_purview_partial_path)
                
        print("\n\nLineage build was a success.\n\n")
        
    except Exception as e:
        print(f"\n\nAn error occurred: {e}\n\n")   


def prod_parse_data_warehouse_table_internal_lineage(client, table_file_name):
    try:
        qualified_name_header = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/"
        #Example: view_file_name = "Inventory.vwDimMarketingResponsibilityHierarchy.sql"
        table = table_file_name.replace(".sql", "").replace(".", "/")
        
        split_source = table.split("/")
        load_routine_file_paths = []
        load_routine_file_path = "data_warehouse_install/Routines/" + split_source[0] + ".Load" + split_source[1] + ".sql"

        if table == "Explore/HBI_UPC_Preferred": # ERROR IN NAMING SCHEMA FOR THIS TABLE LOAD ROUTINE
            load_routine_file_path = "data_warehouse_install/Routines/Explore.LoadUPCPreferred.sql"
        elif table == "Explore/Amz_SalesDiagnostic": # ERROR IN NAMING SCHEMA FOR THIS TABLE LOAD ROUTINE
            load_routine_file_path = "data_warehouse_install/Routines/Explore.LoadAmz_SalesDiagnosticAPI.sql"
        elif table == "Explore/KeplerMediaSpend": # ERROR IN NAMING SCHEMA FOR THIS TABLE LOAD ROUTINE
            load_routine_file_path = "data_warehouse_install/Routines/Explore.Load_KeplerMediaSpend.sql"
        elif table == "stage/DimProduct_Style_Master_1": # ERROR IN NAMING SCHEMA FOR THIS TABLE LOAD ROUTINE
            load_routine_file_path = "data_warehouse_install/Routines/stage.load_DimProductStyleMaster1.sql"
        elif table == "dbo/FactDemand":
            load_routine_file_path = "data_warehouse_install/Routines/dbo.load_FactDemand_SAP.sql"
            # plus add second source
            load_routine_file_paths.append("data_warehouse_install/Routines/dbo.load_FactDemand_STO.sql")
        elif table == "dbo/FactSupply":
            load_routine_file_path = "data_warehouse_install/Routines/dbo.load_FactSupply_OnHand.sql"
            # plus add other sources
            load_routine_file_paths.append("data_warehouse_install/Routines/dbo.load_FactSupply_STO.sql") 
            load_routine_file_paths.append("data_warehouse_install/Routines/dbo.load_FactSupply_Intransit.sql") 
            load_routine_file_paths.append("data_warehouse_install/Routines/dbo.load_FactSupply_WIP.sql") 
            load_routine_file_paths.append("data_warehouse_install/Routines/dbo.load_FactSupply_ChampionManualWIP.sql") 
            load_routine_file_paths.append("data_warehouse_install/Routines/dbo.load_FactSupply_SuggestedWorkOrders.sql") 

        elif table.lower().startswith("master"):
            split_table = table.split("/")
            load_routine_file_path = "data_warehouse_install/Routines/master.load_" + split_table[1] + ".sql"
        elif table.lower().startswith("dbo"):
            split_table = table.split("/")
            load_routine_file_path = "data_warehouse_install/Routines/dbo.load_" + split_table[1] + ".sql"        
        
        load_routine_file_paths.append(load_routine_file_path)

        print(table)

        for routine in load_routine_file_paths:
            sources_for_table = parse_load_routine_for_data_warehouse(routine)
            for source in sources_for_table:
                if source != table: # prevent loop to itself
                    build_table_to_source_data_warehouse_internal_lineage(client, qualified_name_header, table, source)
        
        print("\n\nLineage build was a success.\n\n")
        
    except Exception as e:
        print(f"\n\nAn error occurred: {e}\n\n")   


# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()