import os
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting

try:
    print("Azure App Configuration - Python example")
    # Example code goes here
except Exception as ex:
    print('Exception:')
    print(ex)