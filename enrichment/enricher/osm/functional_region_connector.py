from ..enricher import IEnricherConnector

import pandas as pd
import os
from shapely import wkt
import geopandas
import pyproj
from functools import partial

from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import transform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape, mapping
from rtree import index as rtreeindex

class FunctionalRegionConnector(IEnricherConnector):

    def __init__(self, file, radius, dict_keys):
        self.key = os.path.basename(file).split("-")[0]
        self.value = os.path.basename(file).split("-")[1]
        
        self.radius = radius
        self.dict_keys = dict_keys

        self._df = pd.read_csv(file)
        self._df["geometry"] = self._df["geometry"].apply(wkt.loads)

    def _geodesic_point_buffer(self, lat, lon, radius):
        proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

        # Azimuthal equidistant projection
        aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
        project = partial(
            pyproj.transform,
            pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
            proj_wgs84)
        buf = Point(0, 0).buffer(radius)  # distance in meters
        return transform(project, buf).exterior.coords[:]

    def _get_polygons(self):
        self.array_polygons = []
        for index, row in self._df.iterrows():
            pol = row["geometry"]
            self.array_polygons.append(pol)

        self.idx = rtreeindex.Index()
        for pos, poly in enumerate(self.array_polygons):
            self.idx.insert(pos, poly.bounds)  

    def _fence_check_local(self, point):        
        count = 0
        
        shp = Polygon(self._geodesic_point_buffer(point["latitude"], point["longitude"], self.radius))

        for j in self.idx.intersection(shp.bounds):
            count += 1

        return count        

    def _enrich_point(self, point):      
        amount = self._fence_check_local(point)

        if not self.key is point.keys():
            point[self.key] = amount
        else:
            point[self.key] += amount
        
            
    def enrich(self, data, **kwargs):
        self._get_polygons()

        for d in data.parse(**kwargs):
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