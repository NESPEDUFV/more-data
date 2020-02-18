import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk
from elasticsearch.helpers.errors import BulkIndexError
import parse_geojson

def create_locals_index(client, index):
  with open("./mappings/locals.json", "r") as json_file:
    locals_mapping = json.loads(json_file.read())

  try:
    client.indices.create(index=index, body=locals_mapping)
  except TransportError as e:
    if e.error == "resource_already_exists_exception":
      pass
    else:
      raise

def load_user(client, data, index):
  try:
    for ok, result in streaming_bulk(
        client,
        parse_geojson.parse_local(data),
        index=index,
        chunk_size=500
    ):
        action, result = result.popitem()
        doc_id = "/%s/doc/%s" % (index, result["_id"])
        
        if not ok:
            print("Failed to %s document %s: %r" % (action, doc_id, result))
        else:
            print(doc_id)
  except BulkIndexError as e:
    #log message
    pass
  

def bulk_es_chunks(len, es, data, index):
  for i in range(1, int(len / 500)):
    if i == 1:
      start = i
      end = i * 500
    else : 
      start = end+1
      end += i * 500

    load_user(es, data[start-1 : end], index)

if __name__ == "__main__":
  import os

  es = Elasticsearch(
    hosts=[{'host':'localhost', 'port':9200}]
  )

  create_locals_index (es, "locals")

  # for filename in os.listdir("./data/"):
  with open("./data/shop_mall.geojson", "r") as file:
    data = json.loads(file.read())
    bulk_es_chunks(5000, es, data["features"], "locals")
