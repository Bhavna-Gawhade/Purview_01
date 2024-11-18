from pyapacheatlas.core import AtlasEntity, AtlasException, AtlasClient
import uuid

# Define variables
SERVICE_NAME = "Magento Service"
QUALIFIED_NAME = "magento_service@hbi-qa01-datamgmt-pview"
TYPE_NAME = "Purview_ApplicationService"  # Built-in asset type for Application Service

def create_application_service(client):
    """
    Create an application service entity in Microsoft Purview.

    Args:
        client (AtlasClient): The initialized AtlasClient for Purview.

    Returns:
        dict: The response from the Purview client if successful.
    """
    try:
        # Create an AtlasEntity object for the application service
        app_service = AtlasEntity(
            qualified_name=QUALIFIED_NAME,  # Pass qualified_name as a positional argument
            name=SERVICE_NAME,
            typeName=TYPE_NAME,  # The built-in asset type for Application Service
            guid=f"-{uuid.uuid4()}"  # Optional GUID generation
        )

        # Upload the entity to Purview
        response = client.upload_entities([app_service])
        print("Application service created successfully:", response)
        return response

    except AtlasException as e:
        print("An error occurred while creating the application service:", str(e))
        return None
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return None

from pyapacheatlas.core import AtlasClient

def list_types(client):
    """
    List all available types in the Purview account.

    Args:
        client (AtlasClient): The initialized AtlasClient for Purview.
    """
    try:
        # Retrieve all type definitions
        type_defs = client.get_all_typedefs()
        entity_defs = type_defs.get("entityDefs", [])
        
        for entity_def in entity_defs:
            print(f"Type Name: {entity_def['name']}, Category: {entity_def.get('category', 'No category')}")
    except Exception as e:
        print("An error occurred while listing all asset types:", str(e))

