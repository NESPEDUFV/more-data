from ..enricher import IEnricherConnector
from ...models.data import Data
from ...utils.util import load_json
from typing import Callable, Dict

class ApiConnector(IEnricherConnector):

  def __init__(self, response_parser: Callable, url_pattern: str, params: Dict):
    self.response_parser = response_parser
    self.url_pattern = url_pattern
    self.params = params

  def __make_request(cls, pattern: str, params: Dict, *args, **kwargs):
    import requests
    import re

    regex = re.compile('\{.*?\}')
    routes = regex.findall(pattern)

    for route in routes:
      pattern = pattern.replace(route, params[route[1:len(route)-1]])
    
    return requests.get(pattern).json()

  def enrich(self, data: Data, **kwargs):

    for d in data.parse(**kwargs):
      if self.params["fields"]:
        for field in self.params["fields"]:
          self.params[field["key"]] = d[field["name"]]
      
      yield from self.response_parser(d, self.__make_request(self.url_pattern, self.params))