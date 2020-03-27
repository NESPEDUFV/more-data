from __future__ import annotations
from abc import ABC, abstractproperty, abstractmethod
from typing import Any, List
from .enricher import Enricher
from ..models.data import Data
from pytoolz.functional.pipe import pipe


class Builder(ABC):
    """Design pattern Builder interface
    """

    @abstractmethod
    def with_enrichment(self, connector: Enricher):
        """This method is suppose to add enrichments to :obj:`Data` class
        Parameters
        ----------

        connector: :obj:`Enricher` 
            a connector that will implement enrich method
        """
        pass


class EnricherBuilder(Builder):
    """EnricherBuilder is a class that override Builder interface and for that
    implements abstract method with_enrichment.

    Parameters
    ----------
    data: :obj:`Data`
        Data class is what will be enriched.

    Attributes
    ----------
    data: :obj:`Data`
     
    """

    def __init__(self, data: Data) -> None:
        self._data = data

    def with_enrichment(self, connector: Enricher):
        """Implementation of abstract method of :obj:`Builder`
        Parameters
        ----------

        connector: :obj:`Enricher` 
            a connector that will implement :func:`~enricher.Enricher.enrich`
        """
        self._data.add(connector)
        return self

    def get_result(self):
        """Implements a chaining method like f(g(h(data))). So,
        this method call all of enrichments functions that are 
        saved as array attribute in data class. 
        You can see more of pipe <https://toolz.readthedocs.io/en/latest/api.html#toolz.functoolz.pipe>
        """
        return pipe([e.enrich for e in self._data.enrichers], self._data)
