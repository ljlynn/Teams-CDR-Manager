from azure.cosmos import CosmosClient, exceptions
from pprint import pprint
import yaml
import os


# Construct the relative path of the YAML file
yaml_file = os.path.join(os.path.dirname(__file__), 'config.yaml')

# Open and parse the YAML file
with open(yaml_file, 'r') as f:
    config = yaml.safe_load(f)

# Replace these values with your own
endpoint = config["azure"]["endpoint"]
key = config["azure"]["key"]
database_name = config["azure"]["OperatorCdr"]["database_name"]
container_name = config["azure"]["OperatorCdr"]["container_name"]

# Initialize a CosmosClient instance
client = CosmosClient(endpoint, key)

# Get a reference to the specified database
database = client.get_database_client(database_name)

# Get a reference to the specified container
container = database.get_container_client(container_name)

# Define the data to upload
data = {'callDurationSource': 'microsoft',
        'callId': '6854b348ce305c0884165cbd156ea5cb',
        'callType': 'user_out',
        'calleeNumber': '+1719266837',
        'callerNumber': '+18042560077',
        'charge': 0,
        'conferenceId': None,
        'connectionCharge': 0,
        'currency': 'USD',
        'destinationContext': 'Domestic',
        'destinationName': 'United States',
        'duration': 0,
        'endDateTime': '2023-04-25T15:19:10.2516402Z',
        'id': '008ae8e6-7de2-4963-b208-77462faa76fd',
        'inventoryType': 'Subscriber',
        'licenseCapability': 'MCOPSTN1',
        'operator': None,
        'startDateTime': '2023-04-25T15:19:10.2516402Z',
        'tenantCountryCode': 'US',
        'usageCountryCode': 'US',
        'userDisplayName': 'Melissa Lynn',
        'userId': 'dd558451-ca62-40dd-ba0c-1588afa577e3',
        'userPrincipalName': 'doncamn@lynnlabs.net'}

# Upload the data to the container
try:
    container.upsert_item(data)
    print('Data uploaded successfully')
except exceptions.CosmosHttpResponseError as e:
    pprint(f'Error uploading data: {e.status_code} - {e.message}')