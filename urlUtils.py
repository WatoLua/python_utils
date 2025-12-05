import json
from urllib.parse import urlparse
import requests

localVars = {
    "url_proxy": None
}

def ignoreWarnings():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def withProxy(proxy):
    localVars["url_proxy"] = proxy

def extract_host(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc  # Renvoie le host (nom de domaine ou IP avec port)

def fetchWithJsonV2(method, url, header=None, body=None, printErrors = True):
    requestFunction = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete
    }

    if method.upper() not in requestFunction:
        raise ValueError("Unhandled or invalid HTTP method specified")

    if body == None:
        response = requestFunction[method.upper()](url, headers=header, verify=False, proxies=localVars["url_proxy"])
    else:
        response = requestFunction[method.upper()](url, json=body,
                                                   headers=header, verify=False,
                                                   proxies=localVars["url_proxy"])

    if response.status_code != 200:
        if printErrors:
            print(f"Got error when requested {url} : {response.status_code} : {response.text}")
        return None
    else:
        return json.loads(response.text)

def fetchWithJson(method, url, body=None, printErrors = True):
    requestFunction = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete
    }

    if method.upper() not in requestFunction:
        raise ValueError("Unhandled or invalid HTTP method specified")

    if body == None:
        response = requestFunction[method.upper()](url, verify=False, proxies=localVars["url_proxy"])
    else:
        response = requestFunction[method.upper()](url, json=body,
            headers={"Content-Type": "application/json"}, verify=False, proxies=localVars["url_proxy"])

    if response.status_code != 200:
        if printErrors:
            print(f"Got error when requested {url} : {response.status_code}")
        return None
    else:
        return json.loads(response.text)