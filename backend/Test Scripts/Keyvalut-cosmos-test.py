from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = "https://teamscdrmpv-lynnlabs.vault.azure.net/"
TENANT_ID = "1abc71b9-16f5-43d3-980c-346906ec0e05"
CLIENT_ID = "e22d4fff-fbbd-4ef7-ab37-e98bede1419f"
CLIENT_SECRET = "XUE8Q~z21LaZMTYHgGru6IGo6J__04YzcpMu9dvr"

credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
secret_client = SecretClient(vault_url=VAULT_URL, credential=credential)

cosmos_db_endpoint_uri = secret_client.get_secret("cosmos-endpoint").value
cosmos_db_readwrite_key = secret_client.get_secret("cosmos-readwrite-key").value

print(cosmos_db_endpoint_uri)
print(cosmos_db_readwrite_key)

