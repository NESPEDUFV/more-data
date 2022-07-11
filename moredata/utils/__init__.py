from .osm_downloader import OSM_util

import json
import pyproj
from functools import partial
from shapely.ops import transform
from shapely.geometry import Point, Polygon


def geodesic_point_buffer(lat, lon, radius):
    """This method implements a geodesical point buffering. It creates a circle with radius around the lat/long. It uses the azhimutal projection to fix the problem of distances proportions on globe.

    Parameters
    ----------
    lat: float

    lon: float

    radius: float
        distance in meters
    """
    wgs84 = pyproj.CRS("EPSG:4326")
    merc = pyproj.CRS("EPSG:3857")
    x, y = pyproj.transform(wgs84, merc, lat, lon)
    poly = Polygon(Point(x, y).buffer(radius).exterior.coords[:])

    project = pyproj.Transformer.from_proj(
        pyproj.Proj(init='epsg:3857'),
        pyproj.Proj(init='epsg:4326'))

    poly = transform(project.transform, poly)

    # poly = pyproj.transform(merc,wgs84, poly)

    return poly


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
        with open(file + "-{}.json".format(i), "w") as outfile:
            json.dump(list(group), outfile, ensure_ascii=False)


class Converter:
    @staticmethod
    def json_enriched_to_csv(path, output_path):
        """Get the output of json and converts to csv file.

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
                df = pd.read_json(file, orient="records")
                df.to_csv(output_path + str(i) + ".csv",
                          encoding="utf-8", index=False)
            except AttributeError as e:
                print(file)
                raise (e)

    @staticmethod
    def json_enriched_to_parquet(path, output_path):
        """Get the output of json and converts to parquet file.

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
                df = pd.read_json(file, orient="records")
                df.to_parquet(
                    output_path + str(i) + ".parquet", encoding="utf-8", index=False
                )
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
        df.to_json(output_file, orient="records")
