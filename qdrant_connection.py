from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import pandas as pd

from qdrant_client import QdrantClient

client = QdrantClient(":memory:")

class QDrantConnection(ExperimentalBaseConnection[QdrantClient]):
  def _connect(self):
    print(self._secrets)

    qdrant_client = QdrantClient(
      url=self._secrets['url'],
      api_key=self._secrets['api_key']
    )

    # some error handling...

    # store connected client
    self.qdrant_client = qdrant_client

  def cursor(self) -> QdrantClient:
    return self.qdrant_client
  
  # crete
  def create_collection(self, collection_name: str, vectors_config):
    return self.cursor().recreate_collection(
      collection_name=collection_name,
      vectors_config=vectors_config
    )

  # retrieve

  # get a single collection
  def get_collection(self, collection_name: str):
    return self.cursor().get_collection(collection_name=collection_name)
  
  # get collection with some filtering
  def query(self, collection_name: str, query_vector: str, filter, ttl: int=3600, **kwargs):
    @cache_data(ttl=ttl)
    def _query(collection_name: str, query_vector: str, _filter, **kwargs):
      # default limit as 1
      limit = 1

      if('limit' in kwargs):
        limit = kwargs.pop('limit')
      
      return self.cursor().search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=_filter,
        limit=limit
      )
    
    return _query(collection_name, query_vector, filter, **kwargs)
  
  # update-ish

  # add vectors
  def add_vectors(self, collection_name: str, points):
    return self.cursor().upsert(collection_name=collection_name, wait=True,
      points=points)
  
  # delete
  def delete_collection(self, collection_name: str):
    return self.cursor().delete_collection(collection_name=collection_name)