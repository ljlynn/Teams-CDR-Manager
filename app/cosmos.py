from azure.cosmos import CosmosClient, exceptions

class CosmosDB:
    def __init__(self, url, key, database_name, container_name):
        self.client = CosmosClient(url, credential=key)
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)

    def query(self, query):
        try:
            return 0, list(self.container.query_items(query=query, enable_cross_partition_query=True))
        except exceptions.CosmosHttpResponseError as e:
            return e.status_code, None

    def upsert(self, data):
        error_codes = []

        for item in data['value']:
            # if item contains "@odata"
            try:
                self.container.upsert_item(item)
                error_codes.append(0)
            except exceptions.CosmosHttpResponseError as e:
                error_codes.append(e.status_code)
        return error_codes

    def delete(self, id):
        try:
            self.container.delete_item(id)
            return 0
        except exceptions.CosmosHttpResponseError as e:
            return e.status_code
        
    # function to create new database
    def create_database(self, database_name):
        try:
            self.client.create_database(database_name)
            return 0
        except exceptions.CosmosHttpResponseError as e:
            return e.status_code
        
    # function to create new container
    def create_container(self, container_name):
        try:
            self.database.create_container(container_name)
            return 0
        except exceptions.CosmosHttpResponseError as e:
            return e.status_code
        
    # function to delete container and database
    def delete_container(self, container_name):
        try:
            self.database.delete_container(container_name)
            return 0
        except exceptions.CosmosHttpResponseError as e:
            return e.status_code
        
    def delete_database(self, database_name):
        try:
            self.client.delete_database(database_name)
            return 0
        except exceptions.CosmosHttpResponseError as e:
            return e.status_code
    