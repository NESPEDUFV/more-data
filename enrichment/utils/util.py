import simplejson as json


def read_json_from_file(file):
  with open(file, "r") as f:
    return json.loads(f.read())
  

def load_json(json_object):
  return json.loads(json.dumps(json_object))


def write_json_generator_to_file(file, data):
  with open(file, "w") as f:
    return f.write(json.dumps(data, iterable_as_array=True))
