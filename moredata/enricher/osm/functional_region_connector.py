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

    def __init__(self, files, key, dict_keys=[]):
        self.key = key
        self.dict_keys = dict_keys
        self.files = files

    def _get_polygons(self):
        self.idx = rtreeindex.Index()

        for f in self.files:
            if os.path.getsize(f) > 3:
                print(f)
                _df = pd.read_csv(f)
                _df["geom"] = _df["geom"].apply(wkt.loads) 

                array_polygons = []
                for index, row in _df.iterrows():
                    pol = row["geom"]
                    if isinstance(pol, Polygon) or isinstance(pol, Point):
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
        if "area_point" in point.keys(): 
            amount = self._fence_check_local(point)

            if not self.key in point.keys():
                point[self.key] = amount
            else:
                point[self.key] += amount
        else:
            raise Exception('area_point polygon was not found. Please use function geodesic_point_buffer present in utils package and try again.')
        
            
    def enrich(self, data, **kwargs):
        """Method overrided of interface. It walk through the keys to reach at the data that will be used to intersect the polygons. It uses a R tree to index polygons and search faster. For optimization purposes we recommend to buffer the point, using ``geodesic_point_buffer`` function, creating, necessarily, a label named ``area_point``, and save the file with points buffered to use as base of enrichment. After buffer the points, you can use the Functional Region Connector to create your enrichment passing proper attributes.
        """
        self._get_polygons()
        
        count = 0
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
