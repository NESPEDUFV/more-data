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
class OSMConnector(IEnricherConnector):

    def __init__(self, dict_keys, key, value, place_name="Brasil", file=None, radius=None):
        self.key = key
        self.value = value
        self.place_name = place_name
        self.file = file
        self.radius = radius
        self.dict_keys = dict_keys
        if self.file is not None:
            self._df = pd.read_csv(file)
            self._df["geom"] = self._df["geom"].apply(wkt.loads)

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
        
        if self.radius is not None:
            shp = Polygon(self._geodesic_point_buffer(point["latitude"], point["longitude"], self.radius))
        else:
            shp = Point(point["longitude"], point["latitude"])

        for j in self.idx.intersection(shp.bounds):
            if self.radius is None:
                if shp.within(shape(self.array_polygons[j])):
                    return self._df.iloc[j, ]
            else:
                return self._df.iloc[j].to_frame().T
        return -1        

    def _traverse_dict(self, dict, keys):
        for k in keys:
            try:
                dict = dict[k]
            except KeyError as e:
                return None
        return dict

    def _enrich_point(self, point):      
        polygon_metadata = self._fence_check_local(point)
        
        if not isinstance(polygon_metadata, int):
            polygon_metadata["key"] = self.key
            polygon_metadata["value"] = self.value

            if not "local" in point.keys():
                point["local"] = []
            point["local"].append(*polygon_metadata[["name", "key", "value"]].to_dict("records"))
            
    def enrich(self, data, **kwargs):

        from fiona.crs import from_epsg
        import geopandas

        if self.file is None:
            osm_util = OSM_util()
            self._df = osm_util.get_places(self.place_name, self.key, self.value)

        self._get_polygons()

        for d in data.parse(**kwargs):
            points = d[keys[0]]
            for k in range(1, len(keys)):
                try:
                    points = points[k]
                except KeyError as e:
                    return None

            if isinstance(points, list):
                for point in points:
                    self._enrich_point(point)          
            else:
                self._enrich_point(points)

            yield d        