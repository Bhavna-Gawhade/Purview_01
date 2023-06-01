##! /usr/bin/env python3

# Import Packages
# ---------------
import json


# Import Functions
# ---------------
from modules.managed_attributes import *
from modules.entity import *


# Constants
# ---------------


# Functions
# ---------------

def example_create_and_add_attributes_to_entity():
    # Create an attribute group and attributes
    attribute_group_name = "PRODUCT"
    attribute_names = ["SIZE", "STRUCTURE"]
    response = create_attribute(CLIENT, attribute_group_name, attribute_names)
    print(json.dumps(response))

    # Get an entity
    qualified_name = "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw/Common/DimWinningPortfolioSkuList"
    entity = get_entity_from_qualified_name(qualified_name)
    entity_type = AtlasEntity(
        name = entity["name"],
        typeName = entity["typeName"],
        guid = entity["guid"]
    )

    # Add attribute values to an entity
    attribute_name = "SIZE"
    attribute_value = "15.5"
    response = add_attributes_to_entity(CLIENT, entity_type, attribute_group_name, attribute_name, attribute_value)
    print(json.dumps(response))


# Main Function
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()