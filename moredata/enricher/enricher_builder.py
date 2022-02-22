from abc import ABC, abstractproperty, abstractmethod
from logging import raiseExceptions
from .enricher import Enricher
from ..models.data import Data, JsonData


class Builder(ABC):
    """Design pattern Builder interface"""

    @abstractmethod
    def with_enrichment(self, connector):
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

    def __init__(self, data):
        if isinstance(data, JsonData):
            raise Exception
        self._data = data

    def with_enrichment(self, connector):
        """Implementation of abstract method of :obj:`Builder`
        This method add to :obj:`Data` array attribute :obj:`Enricher` objects

        Parameters
        ----------
        connector: :obj:`Enricher`
            a connector that will implement :func:`~enricher.Enricher.enrich`

        Returns
        -------
        This method return the :obj:`Data`
        """
        self._data.add(connector)
        return self

    def get_result(self, **kwargs):
        def pipe(data, funcs, **kwargs):
            for func in funcs:
                data = func(data=data, **kwargs)
            return data

        """Implements a chaining method like `f(g(h(data)))`. So,
        this method call all of enrichments functions that are 
        saved as array attribute in data class. 

        Returns
        -------
        This method returns the implementations of each :func:`~enricher.Enricher.enrich` that is a Json structure.
        """
        return pipe(self._data, [e.enrich for e in self._data.enrichers], **kwargs)
