from typing import Callable, Dict

class RequestHandler:

  def __init__(self, parser: Callable):
    self.parser = parser

  def parse_request(url: str, *args, **kwargs):
    import requests
    
    # TODO: regex of url and replace {arg} with arg;

    return parser(requests.get(url, params=dict).json())