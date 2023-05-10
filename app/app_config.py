import os

# Application (client) ID of app registration
AUTH_CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
# Application's generated client secret: never check this into source control!
AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")

# You can configure your authority via environment variable
# Defaults to a multi-tenant app in world-wide cloud
AUTHORITY = os.getenv("AUTHORITY", "https://login.microsoftonline.com/common")

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE = "filesystem"
# Using the file system will not work in most production systems,
# it's better to use a database-backed session store instead.

APP_TENANT_ID = os.getenv("APP_TENANT_ID")
APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
APP_CLIENT_SECRET = os.getenv("APP_CLIENT_SECRET")
CDR_COSMOS_OPERATOR_DB_NAME = os.getenv("CDR_COSMOS_OPERATOR_DB_NAME")
CDR_COSMOS_OPERATOR_CONTAINER_NAME = os.getenv("CDR_COSMOS_OPERATOR_CONTAINER_NAME")
CDR_COSMOS_OPERATOR_PARTITION_KEY = os.getenv("CDR_COSMOS_OPERATOR_PARTITION_KEY")
CDR_COSMOS_DR_DB_NAME = os.getenv("CDR_COSMOS_DR_DB_NAME")
CDR_COSMOS_DR_CONTAINER_NAME = os.getenv("CDR_COSMOS_DR_CONTAINER_NAME")
CDR_COSMOS_DR_PARTITION_KEY = os.getenv("CDR_COSMOS_DR_PARTITION_KEY")
CDR_COSMOS_KEY = os.getenv("CDR_COSMOS_KEY")
CDR_COSMOS_ENDPOINT_URI = os.getenv("CDR_COSMOS_ENDPOINT_URI")