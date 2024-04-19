##! /usr/bin/env python3


# Import Functions
# ---------------

from pyapacheatlas.core.util import GuidTracker
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


# Import Packages
# ---------------

from pathlib import Path
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
from datetime import datetime
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
from pathlib import Path
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from typing import Union


# Credential Functions
# ---------------

# Functions
# ---------------

def get_credentials(cred_type: str, client_id: str = None, client_secret: str = None, tenant_id: str = None) -> Union[DefaultAzureCredential, ClientSecretCredential, ServicePrincipalAuthentication]:
    """
    Returns either a DefaultAzureCredential or ClientSecretCredential based on the provided arguments.

    Args:
        cred_type (str): The type of the credentials to create. Can be 'default' or 'client_secret'.
        client_id (str, optional): The client ID of the service principal. Required if cred_type is 'client_secret'.
        client_secret (str, optional): The client secret of the service principal. Required if cred_type is 'client_secret'.
        tenant_id (str, optional): The tenant ID of the service principal. Required if cred_type is 'client_secret'.

    Returns:
        Union[DefaultAzureCredential, ClientSecretCredential]: The created credentials.

    Raises:
        ValueError: If the provided cred_type is not supported or if cred_type is 'client_secret' but client_id, client_secret, or tenant_id are not provided.
    """
    if cred_type == 'default':
        return DefaultAzureCredential(exclude_shared_token_cache_credential=True)
    elif cred_type == 'client_secret':
        if not all([client_id, client_secret, tenant_id]):
            raise ValueError("client_id, client_secret, and tenant_id are required when cred_type is 'client_secret'.")
        return ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    elif cred_type == 'pyapacheatlas_secret':
        if not all([client_id, client_secret, tenant_id]):
            raise ValueError("client_id, client_secret, and tenant_id are required when cred_type is 'client_secret'.")
        return ServicePrincipalAuthentication(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
    else:
        raise ValueError(f"Invalid cred_type provided: {cred_type}")
    

def create_purview_client(credentials: Union[DefaultAzureCredential, ClientSecretCredential, ServicePrincipalAuthentication], purview_account: str, mod_type: str) -> PurviewClient:
    """
    Creates and returns a PurviewClient object authenticated with Azure AD Service Principal.

    Args:
        credentials (Union[DefaultAzureCredential, ClientSecretCredential, ServicePrincipalAuthentication]): The credentials for authentication.
        purview_account (str): The name of the Azure Purview account.
        mod_type (str): The type of python module to use for the operations.

    Returns:
        PurviewClient: An authenticated PurviewClient object.

    Raises:
        ValueError: If an unsupported module type is specified.
        Exception: If an error occurs during the PurviewClient instantiation.
    """
    try:
        # Instantiate the PurviewClient
        if mod_type == 'pyapacheatlas':
            return PurviewClient(account_name=purview_account, authentication=credentials)
        else:
            raise ValueError("Unsupported module type: " + mod_type)
    except Exception as e:
        raise Exception("Error occurred during PurviewClient instantiation.") from e


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
    

def in_progress_get_entity_from_qualified_name(client, qualified_name):
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

def main():
    qual_name = "https://hbipd01analyticsdls.dfs.core.windows.net/curated/Business/US/DimBusiness/"
    entity = in_progress_get_entity_from_qualified_name(qa_client, qual_name)
    print(entity)


  

if __name__ == '__main__':
    main()
