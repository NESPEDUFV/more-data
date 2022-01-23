from geopy.geocoders import Nominatim
from shapely.ops import polygonize
from shapely import geometry
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.ops import linemerge
import requests
import json
import osm2geojson

class OSM_util: 
    def get_place_ID(self, place_name):
        geolocator = Nominatim(user_agent="city_compare")
        geoResults = geolocator.geocode(place_name, exactly_one=False, limit=3, timeout = 600)
        city = None
        for r in geoResults:
            if r.raw.get("osm_type") == "relation":
                city = r
                break
        if city is None:
            raise Exception("city not found")
        place_ID = int(city.raw.get("osm_id")) + 3600000000     #Calcula o ID do local escolhido utilizando\n",
        return place_ID

    def _get_places_overpy(self, query):
        try:
            result = requests.get("http://overpass-api.de/api/interpreter", data={"data":query}).json()
            return osm2geojson.json2geojson(result)
        except:
            return {
                      "features": [],
                      "type": "FeatureCollection"
                    }
        
    
    def get_places(self, place_name, key, value, query=None, tags=("name","geom")):
        if query is None:
            place_id = self.get_place_ID(place_name)
            query = """
            [out:json][timeout:3600];
            area(%s)->.searchArea;
            (
                way[%s=%s](area.searchArea);
                relation[%s=%s](area.searchArea);
            );
            out geom;
            """ % (place_id, key, value, key, value)
        
        result = self._get_places_overpy(query)

        for data in result["features"]:
            properties = data["properties"]
            if "tags" in properties.keys():
                tags = properties["tags"]
                properties['value'] = value
                properties['key'] = key
                for item in tags.items():
                    k, v = item[0], item[1]
                    properties[k]=v
        df = gpd.GeoDataFrame.from_features(result["features"], crs="EPSG:4326")
        return df