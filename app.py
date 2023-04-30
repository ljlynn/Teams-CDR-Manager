import os

from flask import Flask, render_template
from cosmos import CosmosDB

app = Flask(__name__)

TENANT_ID = os.environ.get("TENANT_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CDR_COSMOS_OPERATOR_DB_NAME = os.environ.get("CDR_COSMOS_OPERATOR_DB_NAME")
CDR_COSMOS_OPERATOR_CONTAINER_NAME = os.environ.get("CDR_COSMOS_OPERATOR_CONTAINER_NAME")
CDR_COSMOS_OPERATOR_PARTITION_KEY = os.environ.get("CDR_COSMOS_OPERATOR_PARTITION_KEY")
CDR_COSMOS_DR_DB_NAME = os.environ.get("CDR_COSMOS_DR_DB_NAME")
CDR_COSMOS_DR_CONTAINER_NAME = os.environ.get("CDR_COSMOS_DR_CONTAINER_NAME")
CDR_COSMOS_DR_PARTITION_KEY = os.environ.get("CDR_COSMOS_DR_PARTITION_KEY")
CDR_COSMOS_KEY = os.environ.get("CDR_COSMOS_KEY")
CDR_COSMOS_ENDPOINT_URI = os.environ.get("CDR_COSMOS_ENDPOINT_URI")

operator_cosmos_db = CosmosDB(CDR_COSMOS_ENDPOINT_URI, CDR_COSMOS_KEY, CDR_COSMOS_OPERATOR_DB_NAME, CDR_COSMOS_OPERATOR_CONTAINER_NAME)

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

    # Render the index.html template and pass in the data
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()