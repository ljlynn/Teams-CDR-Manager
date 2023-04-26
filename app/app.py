import markdown
import os
import yaml

from flask import Flask, render_template
from backend.cosmos import CosmosDB



app = Flask(__name__)

# Construct the relative path of the YAML file
# yaml_file = os.path.join(os.path.dirname(__file__), 'config.yaml')

# Open and parse the YAML file
with open('/home/logan/GraphActivitySPA/CDR Manager/app/backend/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

TENANT_ID = config["defaults"]["tenant_id"]
CLIENT_ID = config["defaults"]["client_id"]
CLIENT_SECRET = config["defaults"]["client_secret"]
OPERATOR_CDR_DATABASE = config["azure"]["OperatorCdr"]["database_name"]
OPERATOR_CDR_CONTAINER = config["azure"]["OperatorCdr"]["container_name"]
OPERATOR_CDR_PARTITION_KEY = config["azure"]["OperatorCdr"]["partition_key"]
DR_CDR_DATABASE = config["azure"]["DRCdr"]["database_name"]
DR_CDR_CONTAINER = config["azure"]["DRCdr"]["container_name"]
DR_CDR_PARTITION_KEY = config["azure"]["DRCdr"]["partition_key"]
DB_KEY = config["azure"]["key"]
DB_ENDPOINT_URI = config["azure"]["endpoint"]

operator_cosmos_db = CosmosDB(DB_ENDPOINT_URI, DB_KEY, OPERATOR_CDR_DATABASE, OPERATOR_CDR_CONTAINER)

@app.route('/')
def index():
    # define a query to retrieve all items from the container
    query = "SELECT * FROM c"

    # execute the query
    status_code, results = operator_cosmos_db.query(query)

    # check if the query was successful
    if status_code == 0:
        # pass the results to the template
        return render_template('index.html', data=results)
    else:
        # handle error
        return f"An error occurred while executing the query. Status code: {status_code}"
    
    # # Sample data for the table
        # data = [
        #     {
        #         "id": "02f3d07b-dfe5-42a4-97d0-aa9955bacd26",
        #         "callId": "8240f3d15f915044aac3c9b07fc08e0d",
        #         "userId": "dd558451-ca62-40dd-ba0c-1588afa577e3",
        #         "userPrincipalName": "doncamn@lynnlabs.net",
        #         "userDisplayName": "Melissa Lynn",
        #         "startDateTime": "2023-04-25T15:18:59.2455119Z",
        #         "endDateTime": "2023-04-25T15:18:59.2455119Z",
        #         "duration": "0",
        #         "charge": "0",
        #         "callType": "user_out",
        #         "currency": "USD",
        #         "calleeNumber": "+1917192662837",
        #         "usageCountryCode": "US",
        #         "tenantCountryCode": "US",
        #         "connectionCharge": "0",
        #         "callerNumber": "+18042560077",
        #         "destinationContext": "Domestic",
        #         "destinationName": "United States",
        #         "conferenceId": "None",
        #         "licenseCapability": "MCOPSTN1",
        #         "inventoryType": "Subscriber",
        #         "operator": "None",
        #         "callDurationSource": "microsoft"
        #     },
        #     {
        #         "id": "e7125a5c-1ad3-4b05-898b-84b802a2d900",
        #         "callId": "272925596_130995513@216.82.227.205",
        #         "userId": "fcd019d9-34c1-43c1-846c-cb9370ecdec3",
        #         "userPrincipalName": "marketingrsc@lynnlabsinc.onmicrosoft.com",
        #         "userDisplayName": "marketingrsc",
        #         "startDateTime": "2023-04-12T19:41:22.9965957Z",
        #         "endDateTime": "2023-04-12T19:41:51.9965957Z",
        #         "duration": "29",
        #         "charge": "0",
        #         "callType": "ucap_in",
        #         "currency": "USD",
        #         "calleeNumber": "+12028690277",
        #         "usageCountryCode": "US",
        #         "tenantCountryCode": "US",
        #         "connectionCharge": 0,
        #         "callerNumber": "+19184400850",
        #         "destinationContext": "null",
        #         "destinationName": "null",
        #         "conferenceId": "null",
        #         "licenseCapability": "MCOEV_VIRTUALUSER",
        #         "inventoryType": "Service",
        #         "operator": "null",
        #         "callDurationSource": "microsoft",
        #         "_rid": "4b0FAO9cv8ANAAAAAAAAAA==",
        #         "_self": "dbs/4b0FAA==/colls/4b0FAO9cv8A=/docs/4b0FAO9cv8ANAAAAAAAAAA==/",
        #         "_etag": "\"5f0024a5-0000-0500-0000-6449a4000000\"",
        #         "_attachments": "attachments/",
        #         "_ts": "1682547712"
        #     }]

    # Render the index.html template and pass in the data
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()