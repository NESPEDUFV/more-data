from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

import parser
import models

host = 'localhost'

APP_DATA = "../../datasets/ranking_apps.csv"
USER_DATA = "../../datasets/user_profile_17092019.json"
CENSUS_DATA = "../../datasets/df_census_2010.csv"

LOCALS_DIR = "../../datasets/Locais_OSM/geojson/"
SETORES_DIR = "../../datasets/setores/"

def bulk_user(client):
  user = models.Data(data_file=USER_DATA, parser_func=parser.parsers.parse_user, data_type="json")
  query_user = models.Query(client, "users", "user")
  query_user.load_index(user.parse)

def bulk_app(client):
  app = models.Data(data_file=APP_DATA, parser_func=parser.parsers.csv_generator, data_type="csv")
  query_app = models.Query(client, "apps", "app")
  query_app.load_index(app.parse)

def bulk_locals(client):
  locals = models.Data(data_dir=LOCALS_DIR, parser_func=parser.parsers.parse_local_geojson, data_type="json")
  query = models.Query(client, "locals", "local")
  query.load_index(locals.parse)

def bulk_census_data(client):
  census = models.Data(data_file=CENSUS_DATA, parser_func=parser.parsers.parse_census, data_type="csv")
  query = models.Query(client, "census", "sector")
  query.load_index(census.parse)

def bulk_h3_sectors_data(client, data_type):

  import glob
  dir = SETORES_DIR+"*."+data_type
  files = glob.glob(dir)

  for file in files:
    print(file)
    sector = models.Data(data_file=file, parser_func=parser.parsers.parse_setores, data_type="csv")
    query = models.Query(client, "sectors", "h3_sector")
    query.load_index(sector.parse)

if __name__ == '__main__':
  es = Elasticsearch(
    hosts=[{'host': host, 'port': 9200}]
  )

  # bulk_census_data(es)
  bulk_user(es)
  