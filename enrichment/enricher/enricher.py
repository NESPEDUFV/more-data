from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from ..models.data import Data

class Enricher:
    """Enricher is a wrapper class of interface IEnricherConnector

    Parameters
    ----------
    connector: :obj:`IEnricherConnector`
        Interface that connects an implementation of enrichment to the class :Enricher: 

    Attributes
    ----------
    connector: :obj:`IEnricherConnector`
        Interface that connects an implementation of enrichment to the class :Enricher:   

    """
    def __init__(self, connector: IEnricherConnector) -> None:
        self._connector = connector

    @property
    def connector(self) -> IEnricherConnector:
        """:obj:`IEnricherConnector` getter method
        """
        return self._connector

    @connector.setter
    def connector(self, connector: IEnricherConnector) -> None:
        self._connector = connector

    def enrich(self, data: Data) -> Data:
        """Call enrich function of interface :obj:`IEnricherConnector`
        
        Parameters
        ----------
        data
            :obj:`Data`

        Returns
        -------
        :obj:`Data`
            data enriched

        """
        return self._connector.enrich(data)


class IEnricherConnector(ABC):
    
    @abstractmethod
    def enrich(self, data, **kwargs) -> Data:
        pass