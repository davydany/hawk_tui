from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from typing import List, Dict, Any, Union

from hawk_tui.db_connectors.base import BaseConnection

class ElasticsearchConnection(BaseConnection):
    def __init__(self, host: str, port: int, username: str = None, password: str = None):
        super().__init__(host, port, username, password)
        self.es = None

    def connect(self):
        auth = (self.username, self.password) if self.username and self.password else None
        self.es = Elasticsearch([{'host': self.host, 'port': self.port, 'scheme': 'http'}], http_auth=auth)
        return self.es

    def is_connected(self) -> bool:
        return self.es.ping() if self.es else False

    def close(self):
        if self.es:
            self.es.close()

    # Create
    def insert(self, index: str, document: Dict[str, Any], id: str = None) -> Dict[str, Any]:
        return self.es.index(index=index, body=document, id=id)

    # Read
    def get(self, index: str, id: str) -> Dict[str, Any]:
        try:
            return self.es.get(index=index, id=id)['_source']
        except NotFoundError:
            return None

    def search(self, index: str, query: Dict[str, Any], size: int = 10) -> List[Dict[str, Any]]:
        results = self.es.search(index=index, body=query, size=size)
        return [hit['_source'] for hit in results['hits']['hits']]

    # Update
    def update(self, index: str, id: str, document: Dict[str, Any]) -> Dict[str, Any]:
        return self.es.update(index=index, id=id, body={'doc': document})

    # Delete
    def delete(self, index: str, id: str) -> Dict[str, Any]:
        return self.es.delete(index=index, id=id)

    # Additional useful methods
    def list_indices(self) -> List[str]:
        return list(self.es.indices.get_alias().keys())

    def create_index(self, index: str, mappings: Dict[str, Any] = None) -> Dict[str, Any]:
        return self.es.indices.create(index=index, body={'mappings': mappings} if mappings else None)

    def delete_index(self, index: str) -> Dict[str, Any]:
        return self.es.indices.delete(index=index)

    def bulk_insert(self, index: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        body = []
        for doc in documents:
            body.append({'index': {'_index': index}})
            body.append(doc)
        return self.es.bulk(body=body)

    def count(self, index: str, query: Dict[str, Any] = None) -> int:
        return self.es.count(index=index, body=query if query else {'query': {'match_all': {}}})['count']

    def refresh(self, index: str) -> Dict[str, Any]:
        return self.es.indices.refresh(index=index)

    def get_mapping(self, index: str) -> Dict[str, Any]:
        return self.es.indices.get_mapping(index=index)