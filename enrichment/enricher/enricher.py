from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from models.data import Data

class Enricher:
    def __init__(self, connector: IEnricherConnector) -> None:
        self._connector = connector

    @property
    def connector(self) -> IEnricherConnector:
        return self._connector

    @connector.setter
    def connector(self, connector: IEnricherConnector) -> None:
        self._connector = connector

    def enrich(self, data) -> Data:
        return self._connector.enrich(data)


class IEnricherConnector(ABC):

    @abstractmethod
    def enrich(self, data, **kwargs) -> Data:
        pass