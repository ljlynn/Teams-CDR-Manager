import requests

class Graph:

    def __init__(self, tenant_id, client_id, client_secret):
        
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.resource = "https://graph.microsoft.com"
        self.access_token = self.get_access_token(self.resource)

    def dispaly_tenant_id(self):
        return self.tenant_id
    
    def display_client_id(self):
        return self.client_id
    
    def display_client_secret(self):
        return self.client_secret

    def display_access_token(self):
        return self.access_token


    def get_access_token(self, resource):
        # Define the token url and data
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "resource": resource
        }

        # Get the access token
        token_response = requests.post(token_url, data=token_data)
        token = token_response.json().get("access_token")
        
        return token
    
    def get_OperatorPSTNCallRecords(self, start_date, end_date):

        # Define the graph url and headers
        # Define the base url
        base_url = f"{self.resource}/v1.0/communications/callRecords/getPstnCalls"

        # Add the dates to the url
        graph_url = f"{base_url}(fromDateTime={start_date},toDateTime={end_date})"

        graph_headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        # Get the PSTN calls data
        graph_response = requests.get(graph_url, headers=graph_headers)
        pstn_calls_data = graph_response.json()

        # Print the PSTN calls data
        return pstn_calls_data



    def get_DRPSTNCallRecords(self, start_date, end_date):

        # Define the graph url and headers
        # Define the base url
        base_url = f"{self.resource}/v1.0/communications/callRecords/getDirectRoutingCalls"

        # Add the dates to the url
        graph_url = f"{base_url}(fromDateTime={start_date},toDateTime={end_date})"

        graph_headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        # Get the PSTN calls data
        graph_response = requests.get(graph_url, headers=graph_headers)
        pstn_calls_data = graph_response.json()

        # Print the PSTN calls data
        return pstn_calls_data