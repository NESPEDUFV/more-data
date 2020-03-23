from __future__ import annotations
from abc import ABC, abstractproperty, abstractmethod
from typing import Any, List
from .enricher import Enricher
from models.data import Data

from pytoolz.functional.pipe import pipe

class Builder(ABC):

    @abstractmethod
    def withEnrichment(self, connector: Enricher):
        pass

    @abstractmethod
    def enrich(self) -> Data:
        pass

class EnricherBuilder(Builder):

    def __init__(self, data: Data) -> None:
        self._data = data

    def withEnrichment(self, enricher: Enricher):
        self._data.add(enricher)
        return self

    def get_result(self):
        return pipe([e.enrich for e in self._data.enrichers], self._data)
