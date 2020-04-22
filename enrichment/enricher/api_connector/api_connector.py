from ..enricher import IEnricherConnector
from ...models.data import Data
from ...utils.util import load_json
from typing import Callable, Dict

class ApiConnector(IEnricherConnector):

	def __init__(self, response_parser: Callable, url_pattern: str, params: Dict):
		self.response_parser = response_parser
		self.url_pattern = url_pattern
		self.params = params

	def _handle_params(cls, pattern: str, params: Dict) -> str:
		import re

		regex = re.compile('\{.*?\}')
		routes = regex.findall(pattern)

		for route in routes:
			pattern = pattern.replace(route, params[route[1:len(route)-1]])
		
		return pattern  

	def _make_request(cls, url: str, *args, **kwargs):
		import requests
		from urllib3.exceptions import InsecureRequestWarning
		requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

		return requests.get(url, verify=False).json()

	def enrich(self, data: Data, **kwargs):
		responses_cache = {}

		for d in data.parse(**kwargs):
			if self.params["fields"]:
				for field in self.params["fields"]:
					self.params[field["key"]] = d[field["name"]]

				url = self._handle_params(self.url_pattern, self.params)
				if url in responses_cache.keys():
					response_value = responses_cache[url]
				else:
					response_value = self.response_parser(self._make_request(url))
					responses_cache[url] = response_value

				for k, v in response_value.items():
					d[k] = v

				yield d
