import json
from urllib.parse import urlparse
import requests

def extract_host(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc  # Renvoie le host (nom de domaine ou IP avec port)

def fetchWithJson(method, url, body=None):
    requestFunction = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete
    }

    if method.upper() not in requestFunction:
        raise ValueError("Unhandled or invalid HTTP method specified")

    if body == None:
        response = requestFunction[method.upper()](url, verify=False)
    else:
        response = requestFunction[method.upper()](url, json=body,
            headers={"Content-Type": "application/json"}, verify=False)

    if response.status_code != 200:
        print(f"Got error when requested {url} : {response.status_code}")
        return None
    else:
        return json.loads(response.text)