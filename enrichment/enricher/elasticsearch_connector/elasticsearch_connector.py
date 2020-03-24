from enricher.enricher import IEnricherConnector
from models.data import Data
from .pipeline_handler import Pipeline, PipelineHandler
from .index_handler import ReindexHandler


class ElasticsearchConnector(IEnricherConnector):

    def __init__(self, index_handler, pipeline, reindex_handler):
        self.index_handler = index_handler
        self.pipeline = pipeline
        self.reindex_handler = reindex_handler
    def enrich(self, data: Data) -> Data:

        self.pipeline.create_pipeline()
        self.index_handler.re_index(self.reindex_handler)

        query = {
            "query": {
                "match_all":{}
            }
        }
        
        return self.index_handler.get_all_data(index=self.reindex_handler.target_index, query=query) 
         
