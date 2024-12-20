from typing import List
import requests
import json
from elasticsearch import Elasticsearch

import sys
sys.path.append('C:/Users/mathi/Desktop/informatique/python/utils')
sys.path.append('C:/Users/XTFP190/OneDrive - LA POSTE GROUPE/Documents/python/utils')

import jsonUtils

class ElasticClient:
    url: List[str] = []
    debug: bool

    def __init__(self, urls, debug=False) -> None:
        self.urls = urls
        self.debug = debug

    def exec(self, method: str, endpoint, body=None) -> any:
        return self.runRequest(self.__selectNode(), method, endpoint, body)

    def runRequest(self, url: str, method: str, endpoint, body=None) -> any:
        if url.endswith("/") and not endpoint.startswith("/"):
            endpoint = endpoint[1:]
        if not url.endswith("/") and not endpoint.startswith("/"):
            endpoint = "/" + endpoint

        requestFunction = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete
        }

        if method.upper() not in requestFunction:
            raise ValueError("Unhandled or invalid HTTP method specified")

        if self.debug:
            print(f"call {url + endpoint} with method {method.upper()}")
            print(f"body = {json.dumps(body)}")
        if body == None:
            response = requestFunction[method.upper()](url + endpoint, verify=False)
        else:
            response = requestFunction[method.upper()](url + endpoint, json=body,
                                                       headers={"Content-Type": "application/json"}, verify=False)

        if response.status_code != 200:
            print(f"Got error when requested Elastic search with code {response.status_code}")
            if self.debug:
                print(f"Stack : {response.text}")
            return None
        else:
            return json.loads(response.text)

    def __selectNode(self):
        if len(self.urls) == 1:
            return self.urls[0]
        else:
            for url in self.urls:
                pass

