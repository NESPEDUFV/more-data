import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


from moredata.enricher import Enricher, EnricherBuilder
from moredata.enricher.elasticsearch_connector import (
    ElasticsearchConnector, 
    IndexHandler, 
    ReindexHandler, 
    Pipeline, 
    PipelineHandler,
)
from moredata.models.data import Data
from moredata.parser import parse_document

from elasticsearch import Elasticsearch

HOST = 'localhost'
PORT = 9200

USER_DATA = "../../../datasets/user_profile_processed.json"

if __name__ == "__main__":
    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': PORT}],
        timeout = 10000
    )

    user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json")

    elk_app_enricher = Enricher(connector=ElasticsearchConnector(
        index_handler=IndexHandler(client=es, index="apps-json", doc_type="app"),
        pipeline=Pipeline(client=es,
                          name="user-app",
                          pipeline_handler=PipelineHandler(
                                description="enriching user with apps",
                                match_field="applications_id_list",
                                target_field_name="apps",
                                policy_name="apps-json",
                                max_matches=128)),
        reindex_handler=ReindexHandler(index="users",
                                       target_index="test",
                                       pipeline_name="user-app")))

    user_enriched = \
        EnricherBuilder(user) \
        .with_enrichment(elk_app_enricher) \
        .get_result()
    

    import moredata.utils.util as util
    util.write_json_generator_to_json("../../data/output/json/user-enriched", user_enriched, 1000) 
    util.Converter.json_enriched_to_csv("../../data/output/json/*.json", "../../data/output/csv/")
