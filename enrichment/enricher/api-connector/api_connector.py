from ..enricher import IEnricherConnector
from ...models.data import Data
from typing import Callable

class ApiConnector(IEnricherConnector):

  def __init__(self, parser: Callable):
    self.parser = parser

  def parse_request(self, url: str):
    import requests

    return requests.get(url).json()

  def enrich(self, data: Data, **kwargs):
    return self.parser(data)