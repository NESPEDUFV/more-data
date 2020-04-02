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

def grouper(iterable, n, fillvalue=None):
	from itertools import zip_longest

	args = [iter(iterable)] * n
	return zip_longest(fillvalue=fillvalue, *args)

def write_json_generator_to_json(file, data, n):

	for i, group in enumerate(grouper(data, n)):
		with open(file + '-{}.json'.format(i), 'w') as outfile:
			json.dump(list(group), outfile, ensure_ascii=False)


def convert_json_enriched_to_csv(path, output_path):
	
