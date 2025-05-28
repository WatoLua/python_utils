from symtable import Function
from typing import List
import requests
import json
from elasticsearch import Elasticsearch
import loggingUtils

class ElasticClientHTTP:
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
        if body is None:
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
            #not yet implemented
            return self.urls[0]
            for url in self.urls:
                pass

class ElasticClient:
    def __init__(self, hosts: list[str], logger=loggingUtils.getLogger(__file__)):
        """
        # Initialisation du processeur de donnees
        # Connexion a ES et parametrage des fichiers
        """
        self.es_client = Elasticsearch(hosts)
        self.pit_keep_alive = "20m"
        self.logger = logger
        self.usePit = False

    def create_pit(self, index: str) -> str:
        """
        # Creation du Point in Time pour la recherche
        """
        try:
            pit_response = self.es_client.open_point_in_time(
                index=index,
                keep_alive=self.pit_keep_alive
            )
            return pit_response['id']
        except Exception as e:
            self.logger.error(f"Erreur lors de la creation du PIT: {e}")
            raise

    def forQuery(self, queryConfObject):
        self.queryConf = queryConfObject.copy()
        return self

    def shouldUsePit(self, usePit):
        self.usePit = usePit
        return self

    def execute(self, callbackFunction, **kwargs) -> any:
        """
        # Traitement des documents avec  ou sans PIT
        """
        self.logger.info(f"Search using Pit is set to {self.usePit}")

        pit_id = None
        if self.usePit:
            pit_id = self.create_pit(self.queryConf["index"])
        search_after = None
        total_processed = 0
        page = 0
        try:
            while True:
                page += 1
                query = self.queryConf["query"]
                if search_after:
                    query["search_after"] = search_after

                if self.usePit:
                    # Ajout du PIT dans le body de la requete
                    query.update({"pit": {"id": pit_id, "keep_alive": self.pit_keep_alive}})
                response =(
                    self.es_client.search(
                    body=query,
                )) \
                    if self.usePit \
                    else self.es_client.search(
                    body=query,
                    index=self.queryConf["index"],
                )
                hits = response["hits"]["hits"]
                self.logger.info(f"Nombre de documents trouves : {len(hits)}, page={page}")
                if not hits:
                    break

                for hit in hits:
                    source = hit["_source"]
                    try:
                        total_processed += 1
                        callbackFunction(source, total_processed, **kwargs)

                    except (ValueError, KeyError) as e:
                        self.logger.warning(f"Erreur de traitement du document {source}: {e}")
                        continue

                self.logger.info(f"Nombre total de documents traites: {total_processed}")
                if self.usePit:
                    # Mise a jour du search_after pour la pagination
                    search_after = hits[-1]["sort"]
                else:
                    break

        finally:
            if self.usePit:
                # Nettoyage du PIT
                try:
                    self.es_client.close_point_in_time(body={"id": pit_id})
                except Exception as e:
                    self.logger.error(f"Erreur lors de la suppression du PIT: {e}")

def callbackFuncPrint(doc, count, **kwargs):
    print(count, doc)