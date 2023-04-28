from azure.appconfiguration import AzureAppConfigurationClient
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Set up credentials
credential = DefaultAzureCredential()

# Set up App Configuration client
connection_str = "<your_connection_string>"
app_config_client = AzureAppConfigurationClient.from_connection_string(connection_str)

# Set up Key Vault client
key_vault_uri = "<your_key_vault_uri>"
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

# Retrieve a configuration setting from App Configuration
config_setting = app_config_client.get_configuration_setting(key="TestKey")

# Retrieve a secret from Key Vault
secret_name = "my-secret"
retrieved_secret = secret_client.get_secret(secret_name)
secret_value = retrieved_secret.value

# Use the configuration setting and secret value in your application code
my_setting = config_setting.value
my_secret = secret_value