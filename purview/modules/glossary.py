import json
import os

# PyApacheAtlas packages
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.core.glossary import PurviewGlossaryTerm


# From own files
from purview.utils import get_credentials, create_purview_client
from modules.entity import *


# Constants
# ---------------
# Define constants at the top of the module, 
# in all capital letters with underscores separating words.

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
ENDPOINT = f"https://{REFERENCE_NAME_PURVIEW}.purview.azure.com/"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------



# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 

def main():
    print()

if __name__ == "__main__":
    """
    This sample provides an example of creating a single term.

    In this example, we create Purview terms and have a framework for adding
    a parent term to it as well.
    """

    # Authenticate against your Purview service
    oauth = ServicePrincipalAuthentication(
        tenant_id=os.environ.get("TENANT_ID", ""),
        client_id=os.environ.get("CLIENT_ID", ""),
        client_secret=os.environ.get("CLIENT_SECRET", "")
    )
    client = PurviewClient(
        account_name = os.environ.get("PURVIEW_NAME", ""),
        authentication=oauth
    )

    # When uploading a term, you need to provide which Glossary
    # you are uploading to and that pointer is the guid of the
    # glossary. By default, Purview has one glossary named
    # "Glossary" and the below method will get it for us.
    default_glossary = client.glossary.get_glossary()

    # This is a single term with no hierarchy or term templates
    # you must provide a name, qualifiedName (with an @Glossary
    # at the end).
    term = PurviewGlossaryTerm(
        name="This is my term",
        qualifiedName = "This is my term@Glossary",
        glossaryGuid = default_glossary["guid"],
        longDescription = "This is a long description",
        status = "Draft" # Should be Draft, Approved, Alert, or Expired
    )

    # For this term, I will add a hierarchical term / parent term
    term2 = PurviewGlossaryTerm(
        name="This is my hierarchical term",
        qualifiedName = "This is my hierarchical term@Glossary",
        glossaryGuid = default_glossary["guid"],
        longDescription = "This is a long description",
        status = "Draft" # Should be Draft, Approved, Alert, or Expired
    )
    ## The add_hierarchy method requires the parent formal name
    ## and the parent guid. You should be able to look them up
    ## from the default_glossary["terms"] by iterating over the
    ## list until you find your parent term.
    term2.add_hierarchy(parentFormalName="my parent", parentGuid="xxx-yyy-zzz")

    # For this term, I will add term template attributes
    ## attributes takes in a dictionary that contains a key that
    ## is the name of your term template and has a value that is
    ## another dictionary but contains the attribute names and
    ## values expected for that term template
    term3 = PurviewGlossaryTerm(
        name="This is my template term",
        qualifiedName = "This is my template term@Glossary",
        glossaryGuid = default_glossary["guid"],
        longDescription = "This is a long description",
        status = "Draft", # Should be Draft, Approved, Alert, or Expired
        attributes = {
            "termTemplateName":{
                "attribute1": "xxx",
                "attribute2": "yyy"
            }
        }
    )

    # With the terms defined, you can upload them!
    term_results = client.glossary.upload_term(term)
    # Alternatively, you can upload multiple
    # terms_results = client.glossary.upload_terms([term, term2, term3])

    print(json.dumps(term_results, indent=2))