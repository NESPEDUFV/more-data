from __future__ import annotations
from abc import ABC, abstractproperty, abstractmethod
from typing import Any

class Builder(ABC):

  @abstractproperty
  def data(self) -> None:
    pass

  @abstractmethod
  def withEnrichment(self, IEnricher) -> None:
    pass