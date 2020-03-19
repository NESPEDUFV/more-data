from enrichment.enricher import Enricher, EnricherBuilder
from enrichment.enricher.elasticsearch import ElasticsearchConnector
from enrichment.models.data import Data

if __name__ == '__main__':
    # Model of enrichment framework

    user = Data(None, None, None)

    elk_local_enricher = Enricher(ElasticsearchConnector())
    elk_apps_enricher = Enricher(ElasticsearchConnector())
    elk_census_enricher = Enricher(ElasticsearchConnector())

    user_enriched = \
        EnricherBuilder(user)\
        .withEnrichment(elk_local_enricher)\
        .withEnrichment(elk_apps_enricher)\
        .withEnrichment(elk_census_enricher)\
        .get_result()
