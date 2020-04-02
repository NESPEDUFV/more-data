import os
import sys
sys.path.insert(0, os.path.abspath('..'))


from enrichment.enricher import Enricher, EnricherBuilder
from enrichment.enricher.elasticsearch_connector import ElasticsearchConnector, IndexHandler, ReindexHandler, Pipeline, PipelineHandler, PolicyHandler, Policy
from enrichment.models.data import Data
from enrichment.parser import csv_generator, parse_user
from enrichment.utils.util import read_json_from_file

from elasticsearch import Elasticsearch


ELK_MAPS_DIR = "../elk-maps/"
MAPPING_DIR = ELK_MAPS_DIR + "mappings/"
POLICY_DIR = ELK_MAPS_DIR + "enriches/"

DATASETS_DIR = "../../datasets/"

CIDADES_DIR = DATASETS_DIR + "cidades_info_polygon.csv"
MAPPING_CITY_FILE = MAPPING_DIR + "cities/cities.json"
CITY_POLICY_FILE = POLICY_DIR + "cities-policy.json"

USER_DATA = DATASETS_DIR + "user_profile_17092019.json"

HOST = 'localhost'
PORT = 9200

def bulk_cidades(client):
    cidades = Data(data_file=CIDADES_DIR, parser_func=csv_generator, data_type="csv")
    
    index_handler = IndexHandler(client, "cities", "city")
    mapping = read_json_from_file(MAPPING_CITY_FILE)
    index_handler.create_index(mapping=mapping)

    index_handler.load_index(parser=cidades.parse, streaming=True)

def create_policy(client):
    enrich_fields = ["name", "Nome da Grande Região", "Nome da Mesorregião", "Nome da Microrregião", "Nome da Região Rural"]
    policy = Policy(client, policy_handler=PolicyHandler("geo_match", "cities", "geometry", enrich_fields), name="city-policy")
    policy.create_policy()
    policy.execute_policy()
    

if __name__ == "__main__":
    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': PORT}],
        timeout = 10000
    )

    bulk_cidades(es)
    create_policy(es)

    user = Data(data_file=USER_DATA, parser_func=parse_user, data_type="json")

    elk_city_enricher = Enricher(connector=ElasticsearchConnector(
        index_handler=IndexHandler(client=es, index="cities", doc_type="city"),
        pipeline=Pipeline(client=es,
                          name="user-city-enricher",
                          pipeline_handler=PipelineHandler(
                                description="enriching user with cities",
                                match_field="geo_location",
                                target_field_name="city",
                                policy_name="city-policy",
                                field_array="points_of_interest",
                                shape_relation="CONTAINS")),
        reindex_handler=ReindexHandler(index="u-census-enriched",
                                       target_index="u-city-enriched",
                                       pipeline_name="user-city-enricher")))

    user_enriched = \
        EnricherBuilder(user) \
        .with_enrichment(elk_city_enricher) \
        .get_result()
    
    import enrichment.utils.util as util

    util.write_json_generator_to_json("../data/output/json/user-enriched", user_enriched, 1000) 
    util.convert_json_enriched_to_csv("../data/output/json/*.json", "../data/output/csv/")  
    # this is getting error
    # AssertionError: flatten requires a dictionary input

    