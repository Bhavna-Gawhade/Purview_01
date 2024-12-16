from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient

# Initialize ADF client using Managed Identity
def get_adf_client(subscription_id):
    credential = DefaultAzureCredential()
    client = DataFactoryManagementClient(credential, subscription_id)
    return client

from datetime import datetime, timedelta, timezone

def list_pipeline_runs(client, resource_group_name, factory_name, last_hours=24):
    # Define the time window using timezone-aware UTC objects
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=last_hours)

    # Fetch pipeline runs
    pipeline_runs = client.pipeline_runs.query_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name,
        filter_parameters={
            "lastUpdatedAfter": start_time.isoformat(),
            "lastUpdatedBefore": end_time.isoformat()
        }
    )
    return pipeline_runs.value  # Returns a list of pipeline runs


def list_triggers(client, resource_group_name, factory_name):
    triggers = client.triggers.list_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )
    return [trigger.as_dict() for trigger in triggers]

def list_operations(client):
    operations = client.operations.list()
    return [op.as_dict() for op in operations]

def list_datasets(client, resource_group_name, factory_name):
    datasets = client.datasets.list_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )
    return [dataset.as_dict() for dataset in datasets]

def list_data_flows(client, resource_group_name, factory_name):
    data_flows = client.data_flows.list_by_factory(
        resource_group_name=resource_group_name,
        factory_name=factory_name
    )
    return [data_flow.as_dict() for data_flow in data_flows]

if __name__ == "__main__":
    # Your Azure Data Factory details
    subscription_id = "02bd12d0-66f6-45d0-b12b-4878abfa6b07"
    resource_group_name = "AnalyticsDV-RG"
    factory_name = "hbi-dv01-analytics-df"

    # Initialize client
    adf_client = get_adf_client(subscription_id)

    # List pipeline runs
    pipeline_runs = list_pipeline_runs(adf_client, resource_group_name, factory_name)
    print("\nPipeline Runs:", pipeline_runs)

    # List triggers
    triggers = list_triggers(adf_client, resource_group_name, factory_name)
    print("\nTriggers:", triggers)

    # List operations
    operations = list_operations(adf_client)
    print("\nOperations:", operations)

    # List datasets
    datasets = list_datasets(adf_client, resource_group_name, factory_name)
    print("\nDatasets:", datasets)

    # List data flows
    data_flows = list_data_flows(adf_client, resource_group_name, factory_name)
    print("\nData Flows:", data_flows)
