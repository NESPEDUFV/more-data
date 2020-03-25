from .enricher import Enricher, EnricherBuilder
from .enricher.elasticsearch_connector import ElasticsearchConnector, IndexHandler, ReindexHandler, Pipeline, PipelineHandler
from .models.data import Data
from .parser import parse_user

from elasticsearch import Elasticsearch

HOST = 'localhost'
PORT = 9200

USER_DATA = "../../datasets/user_profile_17092019.json"

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

    user_enriched = \
        EnricherBuilder(user) \
        .with_enrichment(elk_local_enricher) \
        .get_result()

    import utils.util as util
    util.write_json_generator_to_file("../data/output/user-local.json", user_enriched)
