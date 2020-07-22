from geopy.geocoders import Nominatim
from shapely.ops import polygonize
from shapely import geometry
import pandas as pd
import numpy as np
import geopandas as gpd
import overpy
import folium
from shapely.ops import linemerge
import requests
import json
import osm2geojson

class OSM_util: 
    def _get_place_ID(self, place_name):
        geolocator = Nominatim(user_agent="city_compare")
        geoResults = geolocator.geocode(place_name, exactly_one=False, limit=3, timeout = 600)
        for r in geoResults:
            if r.raw.get("osm_type") == "relation":
                city = r
            break

        place_ID = int(city.raw.get("osm_id")) + 3600000000     #Calcula o ID do local escolhido utilizando\n",
        return place_ID

    #Realiza a consulta coletando os três tipos de geometria (Node, Way e Relation) já setando a saída como JSON.
    def _get_places_overpy(self, place_name,key,value): 
        place_id = self._get_place_ID(place_name)
        result = requests.get("http://overpass-api.de/api/interpreter", data={"data":"""
            [out:json][timeout:3600];
            area(%s)->.searchArea;
            (
                way[%s=%s](area.searchArea);
                relation[%s=%s](area.searchArea);
            );
            out geom;
            """ % (place_id, key, value, key, value)}).json()    
        return osm2geojson.json2geojson(result)
    
    def get_places(self, place_name, key, value, tags=("name","geom")):
        
        result = self._get_places_overpy(place_name,key,value)

        for data in result["features"]:
            properties = data["properties"]
            tags = properties["tags"]

            for item in tags.items():
                key, value = item[0], item[1]
                properties[key] = value
        
        df = gpd.GeoDataFrame.from_features(result["features"], crs="EPSG:4326")
        return df