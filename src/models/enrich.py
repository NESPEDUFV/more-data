from elasticsearch.client.ingest import IngestClient
from elasticsearch.client.enrich import EnrichClient

class Enricher:
  
  def __init__(self, client, id, policy, name, pipeline):
    """
      Parameters
      ----------
      client: a elasticsearch client
      id: name for pipeline
      policy: a policy enrichment json
      name: name for policy enrichment
      pipeline: ingest pipeline
    """
    self.policy = policy
    self.pipeline = pipeline
    self.id = id
    self.name = name
    self.ingest_client = IngestClient(client)
    self.enrich_client = EnrichClient(client)
  
  def create_policy(self, params=None):
    try:
      self.enrich_client.put_policy(self.name, self.policy)
    except Exception as e:
      raise(e)
  
  def execute_policy(self, params=None):
    try:
      self.enrich_client.execute_policy(self.name)
    except Exception as e:
      raise(e)
  
  def create_pipeline(self, params=None):
    try:
      self.ingest_client.put_pipeline(self.id, self.pipeline)
    except Exception as e:
      raise(e)