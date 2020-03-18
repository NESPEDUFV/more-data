from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from models.data import Data

class Enricher: 
  def __init__(self, enricher: IEnricher, data: Data) -> None:
    self._enricher = enricher
    self._data = data

  @property
  def enricher(self) -> IEnricher:
    return self._enricher

  @property
  def data(self) -> Data:
    return self._data

  @enricher.setter
  def enricher(self, enricher: IEnricher) -> None:
    self._enricher = enricher

  @data.setter
  def data(self, data: Data):
    self._data = data

  def enrich(self) -> Data: 
    self._enricher.enrich(self.data)


class IEnricher(ABC):

  @abstractmethod
  def enrich(self, data: Data):
    pass