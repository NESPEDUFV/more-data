class Data(list):
  def __init__(self, parser_func, data_type, data_dir=None, data_file=None):
    self.data_dir = data_dir
    self.data_file = data_file
    self.data_type = data_type
    self.parser = parser_func
  
  def read_json(file):
    # TODO: move read_json function to utils package 
    with open(file, "r") as f:
      return json.loads(f.read())
  
  def __iter__(self):
    return self.parser(read_json(self.data_file))

  def parse(self):
    # Plese use data_file arg, data_dir is not implemented correctly here.
    # TODO do data_dir usable.
    if self.data_dir != None:
      import glob
      dir = self.data_dir+"*."+self.data_type
      files = glob.glob(dir)
    
      for file in files:
        return self.parser(file)
    elif self.data_file != None:
      return self.parser(self.data_file)
    else:
      raise Exception("Please, pass a data to parse")

