import simplejson as json


def read_json_from_file(file):
  with open(file, "r") as f:
    return json.loads(f.read())
  

def load_json(json_object):
  return json.loads(json.dumps(json_object))


class StreamArray(list):
  def __init__(self, generator):
    self.generator = generator
    self._len = 1
  
  def __iter__(self):
    self._len = 0
    for item in self.generator:
      yield item
      self._len += 1  
  
  def __len__(self):
    return self._len


def write_json_generator_to_file(file, data):
  with open(file, "w") as outfile:
    stream_array = StreamArray(data)
    for chunk in json.JSONEncoder().iterencode(stream_array):
        outfile.write(chunk)
