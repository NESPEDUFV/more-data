from ..enricher import IEnricherConnector
from ...utils import OSM_util

import pandas as pd
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

from ...utils.util import geodesic_point_buffer
class OSMPlacesConnector(IEnricherConnector):
    """OSMconnector implements interface IEnricherConnector, so this is a connector that can be used to enrich data.
    
    Parameters
    ----------
    dict_keys: List[str]
        dict_keys is the principal argument to the connector. The connector doesn't know where to get data to make the relationship, so you have to pass the keys or if your data isn't nested, just one key to the connector reach at the the right attribute.

    key: str
        class of OSM. eg.: 'amenity', 'leisure'.

    value: str
        value of location of OSM. eg.: 'hospital', 'stadium'.

    place_name: str
        name of local. eg.: 'Brasil', 'São Paulo'.

    file: str, optional
        name of file in CSV of downloaded polygons with must columns: key, value, polygon.

    radius: numeric, optional
        radius to around of point to intersect the polygon.

    Attributes
    ----------
    dict_keys: List[str]

    key: str

    value: str

    place_name: str

    file: str, optional

    radius: numeric, optional
    """

    def __init__(self, key, value, dict_keys=[], place_name="Brasil", file=None, radius=None, geometry_intersected=False):
        self.key = key
        self.value = value
        self.place_name = place_name
        self.file = file
        self.radius = radius
        self.dict_keys = dict_keys
        self.geometry = geometry_intersected
        if self.file is not None:
            self._df = pd.read_csv(file)
            self._df["geometry"] = self._df["geometry"].apply(wkt.loads)

    def _get_polygons(self):
        self.array_polygons = []
        for index, row in self._df.iterrows():
            pol = row["geometry"]
            self.array_polygons.append(pol)

        self.idx = rtreeindex.Index()
        for pos, poly in enumerate(self.array_polygons):
            self.idx.insert(pos, poly.bounds) 

    def _fence_check_local(self, point): 
        polygon_metadata = []
        
        if self.radius is not None:
            shp = Polygon(geodesic_point_buffer(point["latitude"], point["longitude"], self.radius))
        else:
            shp = Point(point["longitude"], point["latitude"])

        for j in self.idx.intersection(shp.bounds):
            if self.radius is None:
                if shp.within(shape(self.array_polygons[j])):
                    polygon_metadata.append(self._df.iloc[j].to_frame().T)
            else:
                polygon_metadata.append(self._df.iloc[j].to_frame().T)
        return polygon_metadata        

    def _traverse_dict(self, dict, keys):
        for k in keys:
            try:
                dict = dict[k]
            except KeyError as e:
                return None
        return dict

    def _enrich_point(self, point):   
        if "latitude" in point.keys() and "longitude" in point.keys():    
            polygon_metadata = self._fence_check_local(point)

            for p in polygon_metadata:
                p["key"] = self.key
                p["value"] = self.value

                if not "local" in point.keys():
                    point["local"] = []
                if not "geometry_intersected" in point.keys() and self.geometry:
                    point['geometry_intersected'] = []

                if self.geometry:
                    polygons_intersected = list(p['geometry'])
                    for polygon in polygons_intersected:
                        point['geometry_intersected'].append(str(polygon))

                point["local"].append(*p[["name", "key", "value"]].to_dict("records"))

    def enrich(self, data, **kwargs):
        """Method overrided of interface. This method do enrichment using OSM data as a enricher. It walk through the keys to reach at the data that will be used to intersect the polygons. It uses a R tree to index polygons and search faster. If the radius attribute is passed the algorithm returns all polygons that intersect the point buffered with this radius else the algorithm returns all polygons that contains the point.
        
        Parameters
        ----------
        data: :obj:`Data`
        """

        from fiona.crs import from_epsg
        import geopandas

        if self.file is None:
            osm_util = OSM_util()
            self._df = osm_util.get_places(self.place_name, self.key, self.value)

        self._get_polygons()

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