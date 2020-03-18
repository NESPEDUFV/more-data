class PolicyHandler:
  def __init__(self, client, policy, name):
    """
      Parameters
      ----------
      client: a elasticsearch client
      policy: a policy enrichment json
      name: name for policy enrichment
    """
    self.policy = policy
    self.name = name
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