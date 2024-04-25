##! /usr/bin/env python3


# Function Imports
# ---------------
#from utils import get_credentials, create_purview_client
#from modules import *
#from modules.lineage.shared_lineage_functions import *
import pandas as pd

# Imports
# ---------------
from pathlib import Path


# Constants
# ---------------


# Functions
# ---------------




def parse_salsify_excel(file):
    '''For a given excel file, iterate through all the sheets and
       create column and entity name mappings.'''
    
    xls = pd.ExcelFile(file)
    salsify_dict={}

    #For each sheet in the given excel
    for sheet_name in xls.sheet_names:

        df = pd.read_excel(file, sheet_name=sheet_name)

        #For every given entity name
        for i in range(len(df['ID'])):

            #Consider only the columns with not nul values
            entity_df=df.iloc[i:i+1,:]
            entity_df=entity_df.dropna(axis=1)
            salsify_dict[df['ID'][i]]=[list(entity_df.columns)]
    return salsify_dict


def parse_salsify_dict(salsify_dict):
    '''Take the output of parse salsify dictionary and create a dataframe
        with column mappings and save it to csv'''
    entity_name_list=[]
    entity_column_list=[]

    for entity_name in salsify_dict:
        lst=salsify_dict[entity_name][0]
        lst.remove('ID')
        #removing strings like - en US , -en AU etc
        lst=[col_name.split('-')[0] for col_name in lst]
        entity_column_list.extend(lst)
        entity_name_list.extend([entity_name]*(len(lst)))
        
    salsify_df=pd.DataFrame({'EntityName':entity_name_list,'EntityColumn':entity_column_list})
    return salsify_df


def save_df_to_csv(df,csv_file_name):
    df.to_csv(csv_file_name)
    return


def get_salsify_descriptions(file_path, col_lst):
    df=pd.read_excel(file_path)
    df=df.loc[:,col_lst]
    return df


    

def main():
    path_to_file= r'C:\Users\Mansi.Choudhary\Documents\Hanes\salsify_export1.xlsx'
    salsify_dict=parse_salsify_excel(path_to_file)
    salsify_df=parse_salsify_dict(salsify_dict)
    file_path=r'C:\Users\Mansi.Choudhary\Documents\Hanes\export_All_Properties_Hanes_Inc.xlsx'
    salsify_desc_df=get_salsify_descriptions(file_path, ['salsify:id','salsify:name'])
    salsify_df=pd.merge(
        salsify_df,salsify_desc_df,left_on='EntityColumn', right_on='salsify:id',how='left')
    salsify_df.drop('salsify:id',axis=1,inplace=True)
    salsify_df.rename(columns={'salsify:name': 'EntityColumnDescription'}, inplace=True)

    salsify_df.to_csv('salsify_final_mappings.csv')
    


if __name__ == '__main__':
    main()

