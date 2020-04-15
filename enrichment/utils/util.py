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

class Converter:
	@staticmethod
	def json_enriched_to_csv(path, output_path):
		import pandas as pd
		from glob import glob
		from flatten_json import flatten

		files = glob(path)

		for i, file in enumerate(files):
			dic_flattened = []
			for d in read_json_from_file(file):
				try:
					dic_flattened.append(flatten(d))
				except AssertionError as e:
					pass
			df = pd.DataFrame(dic_flattened)
			df.to_csv(output_path+str(i)+".csv")

	@staticmethod
	def csv_to_json(file, output_file):
		import csv
		csv.field_size_limit(2147483647)

		arr = []

		with open(file) as f:
			reader = csv.DictReader(f)
			for row in reader:
				arr.append(row)

		with open(output_file, "w+") as out:
			json.dump(arr, out, ensure_ascii=False)