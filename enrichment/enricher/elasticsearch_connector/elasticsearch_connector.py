from enricher.enricher import IEnricherConnector
from models.data import Data
from .pipeline_handler import Pipeline, PipelineHandler
from .index_handler import ReindexHandler


class ElasticsearchConnector(IEnricherConnector):

    def __init__(self, index_handler, pipeline, reindex_handler=None):
        self.index_handler = index_handler
        self.pipeline = pipeline
        self.reindex_handler = reindex_handler
    def enrich(self, data: Data) -> Data:

        self.pipeline.create_pipeline()
        self.index_handler.reindex(self.reindex_handler)

        query = {
            "query": {
                "match_all":{}
            }
        }
        
        data = self.index_handler._scroll_data(index=kwargs.get("target_index"), query=query)

        return data 
         
