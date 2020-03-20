from elasticsearch.client.ingest import EnrichClient


class PolicyHandler:
	def __init__(self, type_match, index, match_field, enrich_fields):
			self._json = {
				type_match: {
					"indices": index,
					"match_field": match_field,
					"enrich_fields": enrich_fields
				}
			}

	def import_json(self):
		pass

	def export_json(self):
		pass

class Policy:

	def __init__(self, client, policy_handler, name):
		"""
		Parameters
		----------
		client: a elasticsearch client
		policy_handler: a policy handler that create json policy
		name: name for policy enrichment
		"""
		self._policy_handler = policy_handler
		self.name = name
		self.enrich_client = EnrichClient(client)
	
	def create_policy(self, params=None):
		try:
			self.enrich_client.put_policy(self.name, self._policy_handler._json)
		except Exception as e:
			raise(e)
	
	def execute_policy(self, params=None):
		try:
			self.enrich_client.execute_policy(self.name)
		except Exception as e:
			raise(e)