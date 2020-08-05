import json

# Load JSON Config Secrets
config_path = '/home/m/config.json'
with open(config_path) as config_json:
    config_dict = json.load(config_json)