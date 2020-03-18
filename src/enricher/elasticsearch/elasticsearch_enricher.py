from elasticsearch.client.enrich import EnrichClient
from enricher import IEnricher
from models.data import Data

class ElasticsearchEnricher(IEnricher):
    
  def enrich(self, data: Data) -> Data:
    #TODO: Create a pipeline and reindex and scroll here.
