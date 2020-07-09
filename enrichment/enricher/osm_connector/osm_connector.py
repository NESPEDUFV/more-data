from ..enricher import IEnricherConnector
from ...utils import OSM_util

import pandas as pd
from shapely import wkt
import geopandas
import pyproj
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import transform as sh_transform
from functools import partial
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape, mapping
from rtree import index as rtreeindex
from shapely.geometry import shape

class OSMConnector(IEnricherConnector):

    def __init__(self, key=None, value=None, place_name="Brasil", file=None, radius=None):
        self.key = key
        self.value = value
        self.place_name = place_name
        self.file = file
        self.radius = radius
        if self.file is not None:
            self._df = pd.read_csv(file)
            self._df["geom"] = self._df["geom"].apply(wkt.loads)

    def _pol_buff_on_globe(self, pol, radius):
        wgs84_globe = pyproj.Proj(proj='latlong', ellps='WGS84')

        _lon, _lat = pol.centroid.coords[0]
        aeqd = pyproj.Proj(proj='aeqd', ellps='WGS84', datum='WGS84',
                        lat_0=_lat, lon_0=_lon)
        project_pol = sh_transform(partial(pyproj.transform, wgs84_globe, aeqd), pol)
        return sh_transform( partial(pyproj.transform, aeqd, wgs84_globe),
                            project_pol.buffer(radius))
            
    def _get_polygons(self):
        self.array_polygons = []
        for index, row in self._df.iterrows():
            pol = row["geom"]
            if self.radius is not None:
                pol = self._pol_buff_on_globe(pol, self.radius)
            self.array_polygons.append(pol)

        self.idx = rtreeindex.Index()
        for pos, poly in enumerate(self.array_polygons):
            self.idx.insert(pos, poly.bounds) 

    def _fence_check_setor(self, point):    
        point = Point(point["longitude"], point["latitude"])
        for j in self.idx.intersection(point.coords[0]):
            print(j)
            if point.within(shape(self.array_polygons[j])):
                return self._df.iloc[j]
        return -1        

    def _traverse_dict(self, dict, keys):
        for k in keys:
            try:
                dict = dict[k]
            except KeyError as e:
                return None
        return dict

    def _enrich_point(self, point):
        
        polygon_metadata = self._fence_check_setor(point)
        if not isinstance(polygon_metadata, int):
            polygon_metadata = polygon_metadata.to_dict()

            if "geom" in polygon_metadata.keys():
                polygon_metadata.pop("geom", None)
            if not "local" in point.keys():
                point["local"] = []
            point["local"].append(polygon_metadata)
        print(point)
        
    def enrich(self, data, **kwargs):
        print(self.value)
        if kwargs.get('keys'):
            keys = kwargs.get('keys')
        else:
            raise Exception

        from fiona.crs import from_epsg
        import geopandas

        if self.file is None:
            osm_util = OSM_util()
        
            self._df = osm_util.get_places(self.place_name, self.key, self.value)
            self._df = geopandas.GeoDataFrame(self._df, geometry='geom')

        self._df.crs = from_epsg(4326)
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