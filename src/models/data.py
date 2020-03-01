class Data:
  def __init__(self, data_dir, parser_func, data_type):
    self.data_dir = data_dir
    self.data_type = data_type
    self.parser = parser_func

  def parse(self):
    # TODO: create kwargs for only file data and data dir
    return self.parser(self.data_dir)

