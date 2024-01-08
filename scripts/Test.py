##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.core import AtlasEntity, AtlasProcess, PurviewClient


# Imports
# ---------------

import re
import sys
import pandas as pd
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


def extract_table_names(sql_query):
    if len(str(sql_query))!=0:
        sql_query=sql_query.replace('[','').replace(']','')
        matches = re.findall(TABLE_NAME_PATTERN, sql_query, re.IGNORECASE)
        table_names = [name for match in matches for name in match if name]
        return (str(list(set(table_names)))[1:-1]).replace("'",'')
 
def extract_qualified_path(tbl_names):
    if len(str(tbl_names))!=0:
        tbl_names=tbl_names.split(',')
        tbl_names = [ele.replace('.', '/') for ele in tbl_names]
        url = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/"
        l = [url+ele for ele in tbl_names]
        return (str(l)[1:-1]).replace("'",'')
 
def main(file_path):
    df=pd.read_excel(file_path)
    df['Query'].fillna('',inplace=True)
    df['Table Names']=df['Query'].apply(extract_table_names)
    df['Table Names'].fillna('',inplace=True)
    df['Fully Qualified Path']=df['Table Names'].apply(extract_qualified_path)
    df.to_excel(file_path,index=False)
 
if __name__=='__main__':
    PROJ_PATH = Path(__file__).resolve().parent
    TABLE_NAME_PATTERN = r'\bFROM\s+([a-zA-Z0-9._]+)|\bJOIN\s+([a-zA-Z0-9._]+)'
    main(r"Lineage inputs\51.15 Stackline Industry Visibility - Weekly Level - ACTIVEWEAR.xlsx")
