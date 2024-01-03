<!-- Improved compatibility of Back to Top link -->
<a name="Azure Databricks-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Scanning Databricks

*Microsoft Purview offers a powerful solution for organizations looking to centralize, manage, and govern their data assets. Integrating Databricks, a popular big data processing and analytics platform, into Purview enhances the data catalog by providing a unified view of Databricks data assets. Registering and scanning Databricks in Purview is a strategic process that empowers organizations to improve data governance, trace data lineage, and enable efficient data discovery.*

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Registering Databricks in Purview](#registering-databricks-in-purview)
- [Configuring Connection Details](#configuring-connection-details)
- [Scanning Databricks Data Assets](#scanning-databricks-data-assets)
- [Verifying Registration and Scanning](#verifying-registration-and-scanning)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Integrating Databricks with Microsoft Purview extends the data catalog to include Databricks data assets, enhancing comprehensive data governance, lineage tracking, and discoverability. This documentation provides step-by-step instructions for registering and scanning Databricks in Purview.

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

## Prerequisites

Ensure the following prerequisites are met before registering and scanning Databricks in Purview:

- Access to the Databricks workspace.
- Purview account with the necessary permissions for Databricks registration.

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

## Registering Databricks in Purview

Registering Databricks in Microsoft Purview is a pivotal step in integrating this powerful big data platform into the broader data ecosystem.Within the Purview portal, users navigate to the "Sources" or "Connectors" section to initiate the registration process. By selecting "Databricks" as the source type, users establish a connection between Purview and their Databricks instance. Providing a unique name for the Databricks source enhances identification within the Purview environment. This registration process lays the foundation for subsequent configuration and scanning activities, enabling comprehensive data governance and cataloging.Save to initiate the registration process.

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

## Configuring Connection Details

Configuring connection details is a crucial step following the successful registration of Databricks in Purview. 

1. After registering, Users locate the registered Databricks source in the Purview portal.
2. Access the configuration settings.
3. Enter the required connection details:
   - Databricks workspace URL
   - Authentication credentials
   - Token or secret key
   - Cluster details, if applicable.
4. Save the configuration.

The accuracy of these details ensures a secure and reliable communication link between Purview and Databricks. Saving the configuration settings solidifies the connection, setting the stage for successful scanning and metadata retrieval.

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

## Scanning Databricks Data Assets

Scanning Databricks data assets is a pivotal process for extracting comprehensive metadata and lineage information. In the "Scans" section of Purview, users initiate a new scan and select the Databricks source. The configuration of scan settings, such as frequency and scope, allows organizations to tailor the scanning process to their specific needs. Executing the scan triggers the retrieval of valuable insights into Databricks data assets, including their characteristics, relationships, and data flow within the Databricks environment. This process is essential for maintaining an up-to-date and accurate catalog of Databricks data within the broader organizational landscape.

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

## Verifying Registration and Scanning

Verifying the registration and scanning processes ensures the successful integration of Databricks into Purview's data catalog and validates the effectiveness of the scanning process. In the "Assets" or "Catalog" section of Purview, users confirm the presence of Databricks data assets. Exploration of metadata and lineage details associated with these assets provides a deeper understanding of their structure, relationships, and data flow. Verification extends to scheduled scans, ensuring they run successfully and consistently update the catalog with the latest information from Databricks. This verification step is crucial for maintaining data governance, accuracy, and transparency across Databricks data assets within the organization.

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

## Troubleshooting

If encountering issues during registration or scanning:

- Check Databricks connection details.
- Review Purview logs for error messages.
- Verify Databricks permissions for the Purview account.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Azure Databricks-top">Back to Top</a>)</p>

