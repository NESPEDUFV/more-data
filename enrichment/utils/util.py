import json


def read_json_from_file(file):
	with open(file, "r") as f:
		return json.loads(f.read())


def load_json(json_object):
	return json.loads(json.dumps(json_object))


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
		""" Get the output of json and converts to csv file.

		Parameters
		----------

		path: str
			path where json files are.
		
		output_path: str
			path where the conversion files will be.
		"""
		import pandas as pd
		from glob import glob

		files = glob(path)

		for i, file in enumerate(files):		
			try:
				df = pd.read_json(file, orient='records')
				df.to_csv(output_path+str(i)+".csv")
			except AttributeError as e:
				pass

	@staticmethod
	def json_enriched_to_parquet(path, output_path):
		""" Get the output of json and converts to parquet file.

		Parameters
		----------

		path: str
			path where json files are.
		
		output_path: str
			path where the conversion files will be.
		"""
		import pandas as pd
		from glob import glob

		files = glob(path)

		for i, file in enumerate(files):		
			try:
				df = pd.read_json(file, orient='records')
				df.to_parquet(output_path+str(i)+".parquet")
			except AttributeError as e:
				pass


	@staticmethod
	def csv_to_json(file, output_file):
		"""Get the output of csv and converts to json file.

		Parameters
		----------

		file: str
			name of file which you want to convert.
		
		output_file: str
			name of output_file.
		"""
		import pandas as pd

		df = pd.read_csv(file)
		df.to_json(output_file, orient="records")
	
	@staticmethod
	def parquet_to_json(file, output_file):
		"""Get the output of parquet and converts to json file.

		Parameters
		----------

		file: str
			name of file which you want to convert.
		
		output_file: str
			name of output_file.
		"""
		import pandas as pd

		df = pd.read_parquet(file)
		df.to_json(output_file, orient='records')
