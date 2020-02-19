import csv

class Parser:
  def __init__(self, data_dir, data_type):
    self.data_dir = data_dir
    self.data_type = data_type
  
  def parser_csv(self):
    with open(data_dir) as f:
      reader = csv.DictReader(f)
      yield reader