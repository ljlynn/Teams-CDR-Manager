import os

from flask import Flask, render_template, redirect
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
dr_cosmos_db = CosmosDB(CDR_COSMOS_ENDPOINT_URI, CDR_COSMOS_KEY, CDR_COSMOS_DR_DB_NAME, CDR_COSMOS_DR_CONTAINER_NAME)

@app.route('/')
def index():
    # define a query to retrieve all items from the container
    op_query = "SELECT * FROM c"

    # execute the query
    status_code, op_results = operator_cosmos_db.query(op_query)

    # define a query to retrieve all items from the container
    dr_query = "SELECT * FROM c"

    # execute the query
    status_code, dr_results = dr_cosmos_db.query(dr_query)

    # check if the query was successful
    if status_code == 0:
        # pass the results to the template
        return render_template('index.html', operator_data=op_results, dr_data=dr_results)
    else:
        # handle error
        return f"An error occurred while executing the query. Status code: {status_code}"

    # Render the index.html template and pass in the data
    return render_template('index.html', data=data)

# create a route that will pull up all details for a specific record
@app.route('/details/<path>/<string:id>')
def call_details(path, id):
    
    # define a query to retrieve the item from the container using id as the filter
    query = f"SELECT * FROM c WHERE c.id = '{id}'"

    # check if the path is "op" or "dr" and execute the query
    if path == "op":
        print("op detected!", path)
        status_code, results = operator_cosmos_db.query(query)
        print(results)

    elif path == "dr":
        print("dr detected!", path)
        status_code, results = dr_cosmos_db.query(query) 
    else:
        return "Invalid path"
        # redirect to /
        return redirect("/")

    return render_template('details.html', type=path, call_details=results)
    

if __name__ == '__main__':
    app.run(debug=True)