from elasticsearch.client.enrich import EnrichClient
from enrichment.enricher.enricher import IEnricherConnector
from enrichment.models.data import Data
from .pipeline_handler import Pipeline, PipelineHandler
from .index_handler import ReindexHandler


class ElasticsearchConnector(IEnricherConnector):

    def __init__(self, index_handler, pipeline):
        self.index_handler = index_handler
        self.pipeline = pipeline

    def enrich(self, data: Data, **kwargs) -> Data:

        self.pipeline.create_pipeline()
        reindex_handler = ReindexHandler(kwargs.get("index"), kwargs.get("target_index"), self.pipeline.name)
        self.index_handler.reindex(reindex_handler)

        self._scroll_data()

        return data

    def _scroll_data(self):
        # TODO: create scroll option
        pass
