from elasticsearch.client.enrich import EnrichClient
from enrichment.enricher.connector import IEnricherConnector
from enrichment.models.data import Data


class ElasticsearchConnector(IEnricherConnector):

    def enrich(self, data: Data) -> Data:
        # TODO: Create a pipeline and reindex and scroll here.
        pass
