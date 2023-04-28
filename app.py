import os

from flask import Flask, render_template
from backend.cosmos import CosmosDB

app = Flask(__name__)

TENANT_ID = os.environ.get("TENANT_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
OPERATOR_CDR_DATABASE = os.environ.get("CDR_COSMOS_OPERATOR_DB_NAME")
OPERATOR_CDR_CONTAINER = os.environ.get("CDR_COSMOS_OPERATOR_CONTAINER_NAME")
OPERATOR_CDR_PARTITION_KEY = os.environ.get("CDR_COSMOS_OPERATOR_PARTITION_KEY")
DR_CDR_DATABASE = os.environ.get("CDR_COSMOS_DR_DB_NAME")
DR_CDR_CONTAINER = os.environ.get("CDR_COSMOS_DR_CONTAINER_NAME")
DR_CDR_PARTITION_KEY = os.environ.get("CDR_COSMOS_DR_PARTITION_KEY")
DB_KEY = os.environ.get("CDR_COSMOS_KEY")
DB_ENDPOINT_URI = os.environ.get("CDR_COSMOS_ENDPOINT_URI")

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

    # Render the index.html template and pass in the data
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()