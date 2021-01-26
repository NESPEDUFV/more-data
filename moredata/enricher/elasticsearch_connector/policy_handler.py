from elasticsearch.client.enrich import EnrichClient
from ...utils import util


class PolicyHandler:
	"""PolicyHandler creates json object for elasticsearch Policy

	Parameters
	----------
	type_match: str
		- geo_match
			enrich data to incoming documents based on a geographic 
			location using a geo_shape query.
		- match
			enrich data to incoming documents based on a precise value, 
			such as an email address or ID, using a term query.
	
	index: str
		name of source index.
	
	match_field: str
		field in the source indices used to match incoming documents.
	
	enrich_fields: array
		fields to add to matching incoming documents. 
		These fields must be present in the source indices
	"""
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
	"""
	A set of configuration options used to add the right 
	enrich data to the right incoming documents 
	(https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-policy-definition.html).

	Parameters
	----------

	client: elasticsearch.Elasticsearch
        a elasticsearch client.
	policy_handler: :obj:`PolicyHandler`
		a policy handler that create json policy
	name: str
		name for policy enrichment

	Attribute
	----------
	
	client: elasticsearch.Elasticsearch
	policy_handler: :obj:`PolicyHandler`
	name: str
	"""

	def __init__(self, client, policy_handler, name):
		
		self._policy_handler = policy_handler
		self.name = name
		self.enrich_client = EnrichClient(client)
	
	def create_policy(self, params=None):
		""" create_policy is a method to create policy file
		"""
		try:
			self.enrich_client.put_policy(self.name, util.load_json(self._policy_handler._json))
		except Exception as e:
			raise(e)
	
	def execute_policy(self, params=None):
		""" execute_policy create the enrich index for an existing enrich policy
		"""
		try:
			self.enrich_client.execute_policy(self.name)
		except Exception as e:
			raise(e)