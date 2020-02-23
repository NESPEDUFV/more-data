import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

from parsers.parser import Parser
from models.query import Query

host = 'localhost'
query_path = 'locals.json'
app_mapping = "../../mappings/points-interests/locals.json"
data = "./data/shop_mall.geojson"

if __name__ == "__main__":
  import os

  es = Elasticsearch(
    hosts=[{'host': host, 'port': 9200}]
  )

  parser = Parser(data, "json")
  query = Query(es, "locals", "document")

  query.create_locals_index(app_mapping)
  query.load_index(parser.parse_local_geojson())
