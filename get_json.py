from urllib import response
import requests
import json
from requests.structures import CaseInsensitiveDict
from requests.models import Response
from datetime import datetime

# Add parameter in the function that will filter the data from api
def get_json(api, token=None, parameters=None):
    headers = CaseInsensitiveDict()
    if token is not None:
        headers["Authorization"] = token
    resp = requests.get(api, headers=headers, verify=False)
    return resp