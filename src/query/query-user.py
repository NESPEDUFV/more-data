import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

from parsers.parser import Parser
from models.query import Query

host = 'localhost'
query_path = 'app.json'
app_mapping = "../../mappings/user/users.json"
data = "../../../datasets/user_profile_17092019.csv"

if __name__ == '__main__':
  es = Elasticsearch(
    hosts=[{'host': host, 'port': 9200}]
  )

  parser = Parser(data, "json")
  query = Query(es, "users", "document")

  query.create_locals_index(app_mapping)
  query.load_index(parser.parser_user())