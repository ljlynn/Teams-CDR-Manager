from azure.cosmos import CosmosClient
import os

# Retrieve the values of the environment variables
endpoint = os.environ['CDR_COSMOS_ENDPOINT_URI']
key = os.environ['CDR_COSMOS_KEY']
database_name = os.environ['CDR_COSMOS_OPERATOR_DB_NAME']
container_name = os.environ['CDR_COSMOS_OPERATOR_CONTAINER_NAME']

# Create a CosmosClient object
client = CosmosClient(endpoint, key)

# Get the database and container objects
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Query the container
query = 'SELECT * FROM c'
items = list(container.query_items(query, enable_cross_partition_query=True))

# Print the results
for item in items:
    print(item)