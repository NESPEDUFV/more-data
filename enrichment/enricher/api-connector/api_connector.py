from ..enricher import IEnricherConnector
from ...models.data import Data
from ...utils.util import read_json_from_file
from typing import Callable, Dict

class ApiConnector(IEnricherConnector):

  def __init__(self, response_parser: Callable, url_pattern: str, params: Dict):
    self.response_handler = response_parser
    self.url_pattern = url_pattern
    self.params = params

  def __make_request(pattern: str, params: Dict, *args, **kwargs):
    import requests
    import re

    regex = re.compile('\{.*?\}')
    routes = regex.findall(pattern)

    for route in routes:
      pattern = pattern.replace(route, params[route[1:len(route)-1]])
    
    return requests.get(pattern).json()

  def enrich(self, data: Data, **kwargs):
    """
      fields: [
        {
          "key": "localidade",
          "name": "id"
        }
      ]
      pesquisa: "-"
      indicador: 49000
      ----------------
      localidade: "id"
    """

    for d in data.parse(**kwargs):
      if params["fields"]:
        for field in params["fields"]:
          params[field["key"]] = d[field["name"]]
        
        del params["fields"]
      
      yield from self.parser(d, self.__make_request(self.url_pattern, params=params))