<!-- Improved compatibility of Back to Top link -->
<a name="Lineage-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Lineage

*Lineage is a critical feature of the Microsoft Purview Data Catalog to support quality, trust, and audit scenarios. The goal of a data catalog is to build a robust framework where all the data systems within your environment can naturally connect and report lineage. Once the metadata is available, the data catalog can bring together the metadata provided by data systems to power data governance use cases. Data lineage is broadly understood as the lifecycle that spans the data’s origin, and where it moves over time across the data estate. It's used for different kinds of backwards-looking scenarios such as troubleshooting, tracing root cause in data pipelines and debugging. Lineage is also used for data quality analysis, compliance and “what if” scenarios often referred to as impact analysis. Lineage is represented visually to show data moving from source to destination including how the data was transformed.*


## Table of Contents

- [Introduction](#introduction)
- [Key Concepts](#key-concepts)
- [Viewing Lineage](#viewing-lineage)
- [Understanding Lineage Diagrams](#understanding-lineage-diagrams)
- [Navigating Lineage Details](#navigating-lineage-details)
- [Filtering Lineage Information](#filtering-lineage-information)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Lineage functionality in Purview enables users to visualize and comprehend the journey of data from its source to destination. It enhances data transparency, governance, and supports informed decision-making.

Microsoft Purview can capture lineage for data in different parts of your organization's data estate, and at different levels of preparation including:

- Raw data staged from various platforms
- Transformed and prepared data
- Data used by visualization platforms

## Key Concepts

- **Lineage Diagram:** A graphical representation of data flow.
- **Source and Destination:** Identifies the origin and endpoint of data.
- **Transformation Nodes:** Represents processes or transformations applied to the data.

## Viewing Lineage

To view lineage in Microsoft Purview:

1. Navigate to the Purview portal.
2. Select a data asset to view its lineage.
3. After accessing asset click on "Lineage" section.

Upon accessing the "Lineage" section of the portal, a rich interface unfolds, revealing a dynamic visual representation of how data traverses through the organization. Users can seamlessly explore and analyze the intricate connections, sources, transformations, and endpoints of their data assets. This intuitive process enhances data transparency and empowers users to make informed decisions by comprehending the complex interplay of data within the organization.

## Understanding Lineage Diagrams

Lineage diagrams within Purview serve as dynamic, graphical narratives of data flow. These diagrams intricately showcase the origin of data, the transformations it undergoes, and its final destinations. Key symbols and connections in the diagrams provide valuable context, allowing users to grasp the chronological sequence of data movement. This understanding is pivotal for stakeholders to gain insights into dependencies, identify potential bottlenecks, and ensure the accuracy and integrity of the data as it evolves throughout its lifecycle.

## Navigating Lineage Details

When exploring lineage details in Purview:

- Click on nodes to view metadata.
- Use zoom and pan features for a comprehensive view.
- Follow connections to trace data flow.

In the "Navigating Lineage Details" phase, users are equipped with interactive tools to delve deeper into the intricacies of data lineage. By clicking on specific nodes within the lineage diagram, users can access detailed metadata associated with each data asset. The platform's user-friendly zoom and pan features facilitate a comprehensive exploration, enabling users to traverse through the lineage graph effortlessly. Following connections between nodes provides a guided journey, revealing the relationships between different data elements and shedding light on the entire data flow landscape.

## Filtering Lineage Information

The ability to filter lineage information is a powerful feature of Purview, allowing users to tailor their analysis to specific parameters. Time-based filters empower users to focus on particular date ranges, aiding in historical analysis and trend identification. Data type filters enable a more granular exploration, honing in on specific categories of data. Directional filters, whether analyzing backward or forward in the data flow, offer flexibility in scrutinizing lineage paths. This nuanced approach to filtering ensures that users can extract meaningful insights from the lineage information, aligning with their analytical goals and organizational needs.

## Best Practices

- **Consistent Naming:** Maintain consistent naming conventions for assets.
- **Regular Lineage Reviews:** Periodically review and update lineage information.
- **Collaboration:** Encourage collaboration between data stakeholders for accurate lineage representation.

## Troubleshooting

If you encounter issues with lineage visualization:

- Check data source connections.
- Review and update metadata for accurate lineage representation.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Lineage-top">Back to Top</a>)</p>