from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

import parser
import models

host = 'localhost'

APP_DATA = "../../datasets/ranking_apps.csv"
USER_DATA = "../../datasets/user_profile_17092019.json"
LOCALS_DIR = "../../datasets/Locais_OSM/geojson/"

if __name__ == '__main__':
  es = Elasticsearch(
    hosts=[{'host': host, 'port': 9200}]
  )

  app = models.Data(data_dir=APP_DATA, parser_func=parser.parsers.parse_app, data_type="csv")
  query_app = models.Query(es, "apps", "app")
  query_app.load_index(app.parse)

  user = models.Data(data_dir=USER_DATA, parser_func=parser.parsers.parse_user, data_type="json")
  query_user = models.Query(es, "users", "user")
  query_user.load_index(user.parse)

  # locals = models.Data(data_dir=LOCALS_DIR, func=parse_local_geojson, data_type="json")
  # query = Query(es, "locals", "local")
  # query.load_index(locals.parse())