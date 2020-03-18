from utils.util import *
from __future__ import annotations
from abc import ABC, abstractproperty, abstractmethod
from typing import Any
class Data:
  def __init__(self, parser_func, data_type, data_file):
    self.data_file = data_file
    self.data_type = data_type
    self.parser = parser_func

  def parse(self):
    return self.parser(self.data_file)

class DataBuilder(Builder):
  def __init__(self, parser_func, data_type, data_file) -> None:
    self.reset(parser_func, data_type, data_file)

  def reset(self, parser_func, data_type, data_file) -> None:
    self._data = Data(parser_func, data_type, data_file)
  
  @property
  def data(self) -> Data:
    data = self.data
    self.reset()
    return data

  def withEnrichment(self, IEnricher):
    pass
