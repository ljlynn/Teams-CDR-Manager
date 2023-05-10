import identity
import identity.web
import requests
import os

from cosmos import CosmosDB
from flask import Flask, render_template, redirect, request, session, session, url_for
from flask_session import Session

import app_config

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config["AUTHORITY"],
    client_id=app.config["AUTH_CLIENT_ID"],
    client_credential=app.config["AUTH_CLIENT_SECRET"],
)


@app.route("/login")
def login():
    return render_template("login.html", version=identity.__version__, **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
    ))


@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))

operator_cosmos_db = CosmosDB(app.config["CDR_COSMOS_ENDPOINT_URI"], app.config["CDR_COSMOS_KEY"], app.config["CDR_COSMOS_OPERATOR_DB_NAME"], app.config["CDR_COSMOS_OPERATOR_CONTAINER_NAME"])
dr_cosmos_db = CosmosDB(app.config["CDR_COSMOS_ENDPOINT_URI"], app.config["CDR_COSMOS_KEY"], app.config["CDR_COSMOS_DR_DB_NAME"], app.config["CDR_COSMOS_DR_CONTAINER_NAME"])

@app.route('/')
def index():
    # check for login
    if not (app.config["AUTH_CLIENT_ID"] and app.config["AUTH_CLIENT_SECRET"]):
        # This check is not strictly necessary.
        # You can remove this check from your production code.
        return render_template('config_error.html')
    if not auth.get_user():
        return redirect(url_for("login"))
    
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