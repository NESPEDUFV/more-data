import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

from parsers.parser import Parser
from models.query import Query

host = 'localhost'
query_path = 'app.json'
app_mapping = "../../mappings/apps/app.json"
csv_data = "../../../datasets/ranking_apps.csv"

if __name__ == '__main__':
  es = Elasticsearch(
    hosts=[{'host': host, 'port': 9200}]
  )

  parser = Parser(csv_data, "csv")
  query = Query(es, "apps", "document")

  query.create_locals_index(app_mapping)
  query.load_index(parser.parser_csv())