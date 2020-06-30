from ..enricher import IEnricherConnector
from ...utils import OSM_util

import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape, mapping
from rtree import index as rtreeindex
from shapely.geometry import shape
import os

class OSM_Connector(IEnricherConnector):

    def __init__(self, key, value, place_name="Brasil"):
        self.key = key
        self.value = value
        self.place_name = place_name
        
    def _get_polygons(self, df):
        self.array_polygons = []
        for index, row in df.iterrows():
            h=shapely.wkt.loads(row["geom"])
            self.array_polygons.append(h)

        self.idx = rtreeindex.Index()
        for pos, poly in enumerate(array_polygons):
            idx.insert(pos, poly.bounds) 

    def _fence_check_setor(self, df, point):    
        point = Point(point)
        for j in self.idx.intersection(point.coords[0]):
            if point.within(shape(self.array_polygons[j])):
                return df.iloc[j]
    return -1

    def _get_dict(self, dict, *keys): # TODO: get and update key
        for k in keys:
            try:
                dict = dict[k]
            except KeyError as e:
                return None
        return dict, keys[len(keys)-1]

    def enrich(self, data, *args, **kwargs):
        from fiona.crs import from_epsg
        import geopandas

        df = OSM_util.get_places(self.key, self.value, self.place_name)
        df = geopandas.GeoDataFrame(df, geometry='geom')
        df.crs = from_epsg(4326)

        self._get_polygons(df)

        for d in data.parse(**kwargs):
            #find 
            point, key = self._get_dict(d, *args)
        pass
        