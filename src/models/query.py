import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk
from elasticsearch.helpers.errors import BulkIndexError

class Query:
  def __init__(self, client, index, doc_type):
    self.client = client
    self.index = index
    self.doc_type = doc_type

  def create_locals_index(self, mapping_file):
    with open(mapping_file, "r") as json_file:
      mapping = json.loads(json_file.read())

    try:
      self.client.indices.create(index=self.index, body=mapping)
    except TransportError as e:
      if e.error == "resource_already_exists_exception":
        pass
      else:
        raise
  
  def load_index(self, parser_func):
    try:
      bulk(
        self.client,
        parser_func(),
        index = self.index,
        doc_type = self.doc_type
      ):
    except BulkIndexError as e:
      #log message
      pass