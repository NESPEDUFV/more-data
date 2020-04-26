import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

import enrichment.parser as parser
import enrichment.models as models
from enrichment.enricher.elasticsearch_connector import IndexHandler
from enrichment.utils.util import read_json_from_file

import parsers

host = 'localhost'

ELK_MAPS_DIR = "../../elk-maps/"
MAPPING_DIR = ELK_MAPS_DIR + "mappings/"

DATASETS_DIR = "../../../datasets/"

APP_DATA = DATASETS_DIR + "ranking_apps.csv"
USER_DATA = DATASETS_DIR + "user_profile_17092019_preprocessed.json"
CENSUS_DATA = DATASETS_DIR + "df_census_2010.csv"

LOCALS_DIR = DATASETS_DIR + "Locais_OSM/geojson/"
SETORES_DIR = DATASETS_DIR + "setores/"

CIDADES_DIR = DATASETS_DIR + "cidades_info_polygon.csv"

MAPPING_LOCAL_FILE = MAPPING_DIR + "points-interests/locals.json"
MAPPING_APPS_FILE = MAPPING_DIR + "apps/app.json"

def bulk_user(client):
    user = models.Data(data_file=USER_DATA, parser_func=parser.parse_document, data_type="json")
    index_handler = IndexHandler(client, "users", "user")
    index_handler.load_index(user.parse, array_point_field="points_of_interest", geo_location=True, code_h3=True)

def bulk_app(client):
    import enrichment.utils.util as util
    util.Converter.csv_to_json(APP_DATA, DATASETS_DIR+"ranking_apps.json")
    app = models.Data(data_file=DATASETS_DIR+"ranking_apps.json", parser_func=parser.parse_document, data_type="csv")
    
    index_handler = IndexHandler(client, "apps-json", "app")

    mapping = read_json_from_file(MAPPING_APPS_FILE)
    index_handler.create_index(mapping=mapping)

    index_handler.load_index(parser=app.parse, streaming=True)    

def bulk_locals(client):
    import enrichment.utils.util as util
    
    index_handler = IndexHandler(client, "locals", "local")
    mapping = read_json_from_file(MAPPING_LOCAL_FILE)

    index_handler.create_index(mapping)

    import glob

    dir = LOCALS_DIR + "*.geojson"
    files = glob.glob(dir)

    for file in files:
        locals = models.Data(data_file=file, parser_func=parsers.parse_local_geojson, data_type="json")
        index_handler.load_index(parser=locals.parse, streaming=True)

def bulk_census_data(client):
    census = models.Data(data_file=CENSUS_DATA, parser_func=parsers.parse_census, data_type="csv")
    index_handler = IndexHandler(client, "census", "sector")
    index_handler.load_index(census.parse)

def bulk_h3_sectors_data(client, data_type):

    import glob
    dir = SETORES_DIR+"*."+data_type
    files = glob.glob(dir)
    
    index_handler = IndexHandler(client, "sectors", "h3_sector")

    for file in files:
        sector = models.Data(data_file=file, parser_func=parser.parsers.parse_setores, data_type="csv")
        index_handler.load_index(sector.parse)

if __name__ == '__main__':
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 9200}]
    )

    # Put your functions here.