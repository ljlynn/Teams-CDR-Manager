import requests
import yaml
import os.path
import pprint

from datetime import datetime, timezone, timedelta
from graph import Graph
from cosmos import CosmosDB

# Construct the relative path of the YAML file
yaml_file = os.path.join(os.path.dirname(__file__), 'config.yaml')

# Open and parse the YAML file
with open(yaml_file, 'r') as f:
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


def get_start_and_end_dates(input_date=datetime.now(tz=timezone.utc), days=30):
    if input_date is None:
        # Get the current date in UTC/GMT timezone
        tz = timezone(timedelta(hours=0))
        # Get the current date and time in UTC as an aware datetime object
        utc_now = datetime.datetime.now(tz)
    else:
        utc_now = input_date
    
    #get date 30 days ago
    utc_start_date_timedelta = utc_now - timedelta(days = 30)

    # add one day to utc_now
    utc_end_date_timedelta = utc_now + timedelta(days = 1)

    #format both date variables as strings
    formatted_end_date = utc_end_date_timedelta.strftime("%Y-%m-%d")
    formatted_start_date = utc_start_date_timedelta.strftime("%Y-%m-%d")

    #print the dates
    print(f"UTC Now: {utc_now}")
    print(f"UTC End Date (+1 day): {formatted_end_date}")
    print(f"UTC Start Date: {formatted_start_date}")

    return formatted_start_date, formatted_end_date


# upload the PSTN call records to Azure Cosmos DB
def upload_PSTNCallRecords(records):
    # upload the PSTN call records to Azure Cosmos DB
    pass


# main function to display records returned from get_psntrecords
def main():
    #get date range for query
    start_date, end_date = get_start_and_end_dates()
    
    # instatiate a new Graph object
    graph = Graph(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    
 

    #print the tenant id
    print("tenant id: " + str(graph.dispaly_tenant_id()))
    #print the client id
    print("client id: " + str(graph.display_client_id()))
    #print the client secret
    print("client secret: " + str(graph.display_client_secret()))
    # display the access token
    print("access token:" + graph.display_access_token())


    operator_json = graph.get_OperatorPSTNCallRecords(start_date, end_date)
    dr_json = graph.get_DRPSTNCallRecords(start_date, end_date)

    # instatiate a new Azure obje5ct
    operator_cosmos_db = CosmosDB(DB_ENDPOINT_URI, DB_KEY, OPERATOR_CDR_DATABASE, OPERATOR_CDR_CONTAINER)

    # upload the PSTN call records to Azure Cosmos DB
    op_resp = operator_cosmos_db.upsert(operator_json)

    dr_cosmos_db = CosmosDB(DB_ENDPOINT_URI, DB_KEY, DR_CDR_DATABASE, DR_CDR_CONTAINER)
    dr_resp = dr_cosmos_db.upsert(dr_json)
    
    print("Operator Cosmos DB Response: " + str(op_resp))
    print("DR Cosmos DB Response: " + str(dr_resp))


if __name__ == "__main__":
    main()