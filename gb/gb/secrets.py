from django.core.exceptions import ImproperlyConfigured

import json
import os

secret_file_path = 'config.json'

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), secret_file_path)) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {setting} setting")