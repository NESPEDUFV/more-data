from ..enricher import IEnricherConnector

import pandas as pd
import os
from shapely import wkt
import geopandas

from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import transform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape, mapping
from rtree import index as rtreeindex
from moredata.models.data import GeopandasData, JsonData, DaskGeopandasData
import dask_geopandas


class FunctionalRegionConnector(IEnricherConnector):
    """FunctionalRegionConnector implements IEnricherConnector interface, so this is a connector that can be used to enrich data. This connector counts how much elements is within a radius of a lat/lon specified by your data.

    Parameters
    ----------
    files: List[str]
        An array of files that will be used to enrich your data. Each file must have 1 attribute, an geometry specifying the polygon to index in RTree.

    dict_keys: List[str]
        The connector doesn't know where to get data to make the relationship, so you have to pass the keys or if your data isn't nested, just one key to the connector reach at the the right attribute.

    key: str
        Key attribute is the name of the new column of your data that stores the counting.

    Attributes
    ----------
    files: List[str]

    dict_keys: List[str]

    key: str
    """

    def __init__(self, files, key, radius=0, dict_keys=[]):
        self.key = key
        self.dict_keys = dict_keys
        self.files = files
        self.radius = radius

        self._df = []
        if self.files is not None:
            read_temp = []
            for file in self.files:
                read_temp.append(pd.read_csv(file))
            self._df = pd.concat(read_temp)
            self._df["geometry"] = self._df["geometry"].apply(wkt.loads)
            self._df = geopandas.GeoDataFrame(self._df)

    def _get_polygons(self):
        self.idx = rtreeindex.Index()

        for f in self.files:
            array_polygons = []
            for index, row in self._df.iterrows():
                pol = row["geometry"]
                if isinstance(pol, Polygon) or isinstance(pol, Point):
                    array_polygons.append(pol)

            for pos, poly in enumerate(array_polygons):
                self.idx.insert(pos, poly.bounds)

    def _fence_check_local(self, point):
        count = 0

        shp = wkt.loads(point["area_point"])
        for j in self.idx.intersection(shp.bounds):
            count += 1
        return count

    def _enrich_point(self, point):
        if "area_point" in point.keys():
            amount = self._fence_check_local(point)

            if not self.key in point.keys():
                point[self.key] = amount
            else:
                point[self.key] += amount
        else:
            raise Exception(
                "area_point polygon was not found. Please use function geodesic_point_buffer present in utils package and try again."
            )

    def enrichJsonData(self, data, **kwargs):
        for d in data.parse(**kwargs):

            if not self.dict_keys:
                points = d
            else:
                points = d[self.dict_keys[0]]
                for k in range(1, len(self.dict_keys)):
                    try:
                        points = points[self.dict_keys[k]]
                    except KeyError as e:
                        return None

            if isinstance(points, list):
                for point in points:
                    self._enrich_point(point)
            else:
                self._enrich_point(points)

            yield d

    def _buffer_with_crs(self, data, new_crs=None):
        if new_crs is None:
            new_crs = "EPSG:3857"

        if data.crs is None:
            data = data.set_crs("EPSG:4326")

        data["geometry_not_buffered"] = data["geometry"].copy()

        if data.crs != new_crs:
            data = data.to_crs(new_crs)

        data["geometry"] = data["geometry"].buffer(self.radius)

        data = data.to_crs("EPSG:4326")

        return data

    def enrich_geopandas_data(self, data: geopandas.GeoDataFrame, **kwargs):
        self._df = self._df.set_crs("EPSG:4326")
        data.reset_index(inplace=True)

        if self.radius != 0:
            data = self._buffer_with_crs(data, kwargs.get("new_crs", None))

        spatial_joined = geopandas.sjoin(
            data, self._df, how="inner", predicate="intersects"
        )
        different_indices = spatial_joined.index.value_counts()

        data.set_index("index", inplace=True)

        data[self.key] = different_indices
        data[self.key].fillna(0, inplace=True)

        data["geometry"] = data["geometry_not_buffered"]
        data.drop("geometry_not_buffered", axis=1, inplace=True)

        return GeopandasData.from_geodataframe(data)

    def enrich_dask_geopandas_data(self, data, **kwargs):
        self._df = self._df.set_crs("EPSG:4326")
        data.reset_index(inplace=True)

        if not "geometry_not_buffered" in data.columns:
            data = self._buffer_with_crs(data, kwargs.get("new_crs", None))

        self._df = self._df.set_crs("EPSG:4326")

        joined = dask_geopandas.sjoin(data, self._df, predicate="intersects")

        return DaskGeopandasData.from_dask_geodataframe(joined)

    def enrich(self, data, **kwargs):
        """Method overrided of interface. It walk through the keys to reach at the data that will be used to intersect the polygons. It uses a R tree to index polygons and search faster. For optimization purposes we recommend to buffer the point, using ``geodesic_point_buffer`` function, creating, necessarily, a label named ``area_point``, and save the file with points buffered to use as base of enrichment. After buffer the points, you can use the Functional Region Connector to create your enrichment passing proper attributes."""
        self._get_polygons()

        if isinstance(data, GeopandasData):
            return self.enrich_geopandas_data(data.data, **kwargs)

        elif isinstance(data, DaskGeopandasData):
            raise self.enrich_dask_geopandas_data(data.data, **kwargs)

        elif isinstance(data, JsonData):
            return self.enrichJsonData(data, **kwargs)
