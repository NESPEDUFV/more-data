import os
import sys
sys.path.insert(0, os.path.abspath('..'))


from enrichment.enricher import Enricher, EnricherBuilder
from enrichment.enricher.elasticsearch_connector import ElasticsearchConnector, IndexHandler, ReindexHandler, Pipeline, PipelineHandler
from enrichment.models.data import Data
from enrichment.parser import parse_user

from elasticsearch import Elasticsearch

HOST = 'localhost'
PORT = 9200

USER_DATA = "../datasets/user_profile_17092019.json"

if __name__ == '__main__':

    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': PORT}],
        timeout = 10000
    )

    user = Data(data_file=USER_DATA, parser_func=parse_user, data_type="json")

    elk_local_enricher = Enricher(connector=ElasticsearchConnector(
        index_handler=IndexHandler(client=es, index="locals", doc_type="local"),
        pipeline=Pipeline(client=es,
                          name="user-local-enricher",
                          pipeline_handler=PipelineHandler(
                                description="enriching user with locals",
                                match_field="geo_location",
                                target_field_name="local",
                                policy_name="locals-policy",
                                field_array="points_of_interest",
                                shape_relation="CONTAINS")),
        reindex_handler=ReindexHandler(index="users",
                                       target_index="u-local-enriched",
                                       pipeline_name="user-local-enricher")))

    elk_app_enricher = Enricher(connector=ElasticsearchConnector(
        index_handler=IndexHandler(client=es, index="apps", doc_type="app"),
        pipeline=Pipeline(client=es,
                          name="user-app-enricher",
                          pipeline_handler=PipelineHandler(
                                description="enriching user with locals",
                                match_field="applications_id_list",
                                target_field_name="apps",
                                policy_name="app-user-policy",
                                max_matches=128)),
        reindex_handler=ReindexHandler(index="u-local-enriched",
                                       target_index="u-app-enriched",
                                       pipeline_name="user-app-enricher")))

    elk_sector_enricher = Enricher(connector=ElasticsearchConnector(
        index_handler=IndexHandler(client=es, index="sectors", doc_type="sector"),
        pipeline=Pipeline(client=es,
                          name="user-sector-enricher",
                          pipeline_handler=PipelineHandler(
                                description="enriching user with setor_id",
                                match_field="code_h3",
                                target_field_name="sectors",
                                policy_name="sector-policy",
                                field_array="points_of_interest")),
        reindex_handler=ReindexHandler(index="u-app-enriched",
                                       target_index="u-sector-enriched",
                                       pipeline_name="user-sector-enricher")))
    
    elk_census_enricher = Enricher(connector=ElasticsearchConnector(
        index_handler=IndexHandler(client=es, index="census", doc_type="census"),
        pipeline=Pipeline(client=es,
                          name="user-census-enricher",
                          pipeline_handler=PipelineHandler(
                                description="enriching user with census",
                                match_field="sectors.setor_id",
                                target_field_name="sectors.census",
                                policy_name="census-policy",
                                field_array="points_of_interest",
                                max_matches=10)),
        reindex_handler=ReindexHandler(index="u-sector-enriched",
                                       target_index="u-census-enriched",
                                       pipeline_name="user-census-enricher")))
    user_enriched = \
        EnricherBuilder(user) \
        .with_enrichment(elk_local_enricher) \
        .with_enrichment(elk_app_enricher) \
        .with_enrichment(elk_sector_enricher) \
        .with_enrichment(elk_census_enricher) \
        .get_result()
    

    import enrichment.utils.util as util
    util.write_json_generator_to_file("../data/output/user-enriched.json", user_enriched)
