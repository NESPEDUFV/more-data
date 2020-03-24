class Data:
  def __init__(self, parser_func, data_type, data_file):
    self.data_file = data_file
    self.data_type = data_type
    self.parser = parser_func
    self.enrichers = []

  def parse(self):
    return self.parser(self.data_file)

  def add(self, enricher) -> None:
    self.enrichers.append(enricher)
