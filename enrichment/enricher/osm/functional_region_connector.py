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

    def __init__(self, files, radius, key, dict_keys):
        self.key = key
        self.radius = radius
        self.dict_keys = dict_keys
        self.files = files

    def _get_polygons(self):
        self.idx = rtreeindex.Index()

        for f in self.files:
            if os.path.getsize(f) > 3:
                _df = pd.read_csv(f)
                _df["geometry"] = _df["geometry"].apply(wkt.loads)  

                array_polygons = []
                for index, row in _df.iterrows():
                    pol = row["geometry"]
                    array_polygons.append(pol)

                for pos, poly in enumerate(array_polygons):
                    self.idx.insert(pos, poly.bounds)  

    def _fence_check_local(self, point):        
        count = 0
        
        shp=wkt.loads(point["area_point"])
        for j in self.idx.intersection(shp.bounds):
            count += 1
        return count        

    def _enrich_point(self, point):  
        if "latitude" in point.keys() and "longitude" in point.keys(): 
            amount = self._fence_check_local(point)

            if not self.key in point.keys():
                point[self.key] = amount
            else:
                point[self.key] += amount
        
            
    def enrich(self, data, **kwargs):
        self._get_polygons()
        
        count = 0
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