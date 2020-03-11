import json
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk
from elasticsearch.helpers.errors import BulkIndexError

class Query:
  def __init__(self, client, index, doc_type):
    self.client = client
    self.index = index
    self.doc_type = doc_type

  def create_index(self, mapping):
    try:
      self.client.indices.create(index=self.index, body=mapping)
    except TransportError as e:
      if e.error == "resource_already_exists_exception":
        pass
      else:
        raise
  
  def load_index(self, parser, streaming=None):
    try:
      if streaming:
        for ok, response in streaming_bulk(self.client, index=self.index, actions = parser()):
          if not ok:
            # failure inserting
            print(response)
      else: 
          bulk(
            self.client,
            parser(),
            index = self.index,
            doc_type = self.doc_type
          ) 
    except BulkIndexError as e:
      pass
    
