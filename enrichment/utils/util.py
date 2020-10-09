import json
import pyproj
from functools import partial
from shapely.ops import transform
from shapely.geometry import Point

def geodesic_point_buffer(lat, lon, radius):
	"""This method implements a geodesical point bufferization. It creates a circle with radius around the lat/long. It uses the azhimutal projection to fix the problem of distances proportions on globe.

	Parameters
	----------
	lat: float

	lon: float

	radius: float
		distance in meters
	"""
	proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

	# Azimuthal equidistant projection
	aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
	project = partial(
		pyproj.transform,
		pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
		proj_wgs84)
	buf = Point(0, 0).buffer(radius)  # distance in meters
	return transform(project, buf).exterior.coords[:]

def read_json_from_file(file):
	with open(file, "r") as f:
		return json.loads(f.read())

def load_json(json_object):
	return json.loads(json.dumps(json_object))

def chunks(iterable, size=10):
	from itertools import chain, islice
	iterator = iter(iterable)
	for first in iterator:
		yield chain([first], islice(iterator, size - 1))

def write_json_generator_to_json(file, data, n):
	for i, group in enumerate(chunks(data, n)):
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
		import json
		from glob import glob

		files = glob(path)

		for i, file in enumerate(files):
			try:
				df = pd.read_json(file, orient='records')
				df.to_csv(output_path+str(i)+".csv", encoding='utf-8', index=False)
			except AttributeError as e:
				print(file)
				raise(e)

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
				df.to_parquet(output_path+str(i)+".parquet", encoding='utf-8', index=False)
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
