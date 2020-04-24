from ..enricher import IEnricherConnector
from ...models.data import Data
from .pipeline_handler import Pipeline, PipelineHandler
from .index_handler import ReindexHandler


class ElasticsearchConnector(IEnricherConnector):
    """ElasticsearchConnector implements interface IEnricherConnector, 
    so this is a connector that can be used to enrich some data. 
    ElasticsearchConnector implements handlers for `index`, `pipeline` and `policy`,
    all are requirement to enrich your data using elasticsearch. 

    Parameters
    ----------
    index_handler: :obj:`IndexHandler`
        control index actions in elasticsearch
    
    pipeline: :obj:`Pipeline`
        control pipeline actions in elasticsearch
    
    reindex_handler: :obj:`ReindexHandler`
        control reindexing in elasticsearch

    Attributes
    ----------
    index_handler: :obj:`IndexHandler`

    pipeline: :obj:`Pipeline`
    
    reindex_handler: :obj:`ReindexHandler`
    """
    def __init__(self, index_handler, pipeline, reindex_handler):
        self.index_handler = index_handler
        self.pipeline = pipeline
        self.reindex_handler = reindex_handler

    def enrich(self, data, **kwargs):
        """Method overrided of interface. This interface do enrichment using 
        elasticsearch as a enricher: create a pipeline, reindex with a pipeline
        specified to enrich and return all data enriched as Json.

        Parameters
        ----------
        data: :obj:`Data`
        """

        self.pipeline.create_pipeline()
        self.index_handler.re_index(self.reindex_handler)
        
        return self.index_handler.get_all_data(index=self.reindex_handler.target_index, **kwargs) 
         
