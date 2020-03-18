from elasticsearch.client.ingest import IngestClient

class Pipeline:
  
  def __init__(self, client, id, pipeline):
    """
      Parameters
      ----------
      client: a elasticsearch client
      id: name for pipeline
      pipeline: ingest pipeline
    """
    self.pipeline = pipeline
    self.id = id
    self.ingest_client = IngestClient(client)
  
  def create_pipeline(self, params=None):
    try:
      self.ingest_client.put_pipeline(self.id, self.pipeline)
    except Exception as e:
      raise(e)