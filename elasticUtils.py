from symtable import Function
from typing import List
import requests
import json
from elasticsearch import Elasticsearch
import loggingUtils

def cycle_from_to(from_, to):
    n = from_
    while True:
        yield n
        n = (n + 1) % to

class ElasticClientHTTP:
    url: List[str] = []
    debug: bool

    def __init__(self, urls, debug=False) -> None:
        self.urls = urls
        self.debug = debug
        self.index_url = cycle_from_to(0, len(self.urls))

    def exec(self, method: str, endpoint, body=None) -> any:
        return self.runRequest(self.__selectNode(), method, endpoint, body)

    def runRequest(self, url: str, method: str, endpoint, body=None) -> any:
        if url.endswith("/") and endpoint.startswith("/"):
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
            return self.urls[next(self.index_url)]

class ElasticClient:
    def __init__(self, hosts: list[str], logger=loggingUtils.getDefaultLogger(), keepAlive="20m"):
        """
        # Initialisation du processeur de donnees
        # Connexion a ES et parametrage des fichiers
        """
        self.es_client = Elasticsearch(hosts)
        self.pit_keep_alive = keepAlive
        self.logger = logger
        self.usePit = False
        self.total_hits = -1
        self.threshold_hits = -1
        self.max_hits_to_process = -1

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

    def add_default_sort_if_missing(self):
        if "sort" not in self.queryConf["query"]:
            self.queryConf["query"]["sort"] = [{ "_shard_doc": "asc" }]
        return self

    def cut_search_at(self, max_hits_to_process):
        self.max_hits_to_process = max_hits_to_process
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
        self.threshold_hits = 0
        page = 0
        try:
            continue_search = True
            while continue_search:
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
                if page == 1:
                    self.total_hits = response['hits']['total']['value']
                    self.logger.info(f"Nombre total de documents : {self.total_hits}")
                self.logger.info(f"Nombre de documents trouves : {len(hits)}, page={page}")
                if not hits:
                    break

                for hit in hits:
                    try:
                        if self.max_hits_to_process != -1 and self.threshold_hits >= self.max_hits_to_process:
                            continue_search = False
                            break
                        self.threshold_hits += 1
                        callbackFunction(hit, self.threshold_hits, **kwargs)

                    except (ValueError, KeyError) as e:
                        self.logger.exception(f"Erreur de traitement du document {hit}: {e}")
                        continue

                self.logger.info(f"Nombre total de documents traites: {self.threshold_hits}")
                if self.usePit:
                    if "sort" in self.queryConf["query"]:
                        # Mise a jour du search_after pour la pagination
                        search_after = hits[-1]["sort"]
                    else:
                        self.logger.error("La recherche ne contient pas de sort, la pagination ne fonctionnera pas.\n Utiliser add_default_sort_if_missing() pour un trie par défault")
                else:
                    break
        except Exception as e:
            self.logger.exception(f"Erreur lors du traitement: {e}")
        finally:
            if self.usePit:
                # Nettoyage du PIT
                try:
                    self.es_client.close_point_in_time(body={"id": pit_id})
                except Exception as e:
                    self.logger.exception(f"Erreur lors de la suppression du PIT: {e}")
        return self.threshold_hits

def callbackFuncPrint(doc, count, **kwargs):
    print(count, doc)