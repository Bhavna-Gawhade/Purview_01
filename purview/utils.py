##! /usr/bin/env python3
"""
    Objects & Methods
    ---------

    Sample Invocation
    ---------

"""

# File Notes
__author__ = "User Name"
__version__ = "1.0"
__email__ = "dylan.gregorysmith@gmail.com"
__status__ = "Development"

# Imports
# ---------------
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json
from pathlib import Path
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from typing import Union

# Constants
# ---------------
# Define constants at the top of the module, 
# in all capital letters with underscores separating words.

CONSTANT_1 = 'X'
CONSTANT_2 = 'Y'

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
        return DefaultAzureCredential()
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
        mod_type (str): The type of python module to use for the operations
        tenant_id (str): The Azure AD tenant ID.
        client_id (str): The client ID (Application ID) of the Azure AD Service Principal.
        client_secret (str): The client secret (Application Secret) of the Azure AD Service Principal.
        purview_account (str): The name of the Azure Purview account.

    Returns:
        PurviewClient: An authenticated PurviewClient object.
    """
    # Instantiate the PurviewClient
    if mod_type == 'pyapacheatlas':
        return PurviewClient(account_name=purview_account, authentication=credentials)
    
def save_dict_to_json(data: dict, path: Path, filename: str):
    """
    Save a dictionary to a JSON file nested within the current directory.

    Args:
        data (dict): The dictionary to be saved.
        filename (str): The name of the JSON file.
    """
    # Convert the dictionary to JSON format
    json_data = json.dumps(data, indent=2)


    # Create a Path object for the output file
    file_path = path.joinpath(filename)

    # Write the JSON data to the file
    with file_path.open(mode='w') as file:
        file.write(json_data)