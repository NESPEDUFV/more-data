from geopy.geocoders import Nominatim
from shapely.ops import polygonize
from shapely import geometry
import pandas as pd
import numpy as np
import geopandas
import overpy
import folium
from shapely.ops import linemerge
import requests
import json

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
        api = overpy.Overpass()
        result = api.query("""
            [out:json][timeout:3600];
            area(%s)->.searchArea;
            (
              way[%s=%s](area.searchArea);
              relation[%s=%s](area.searchArea);
            );
            out geom;
            """ % (place_id,key,value,key,value))
        return result
    
    #Corrige polígonos que são formados por vários polígonos 
    def _to_polygon(self, geom, geom_size):
        if geom_size > 1: #Se possui somente uma componente não faz nada
            try:
                geom = geometry.Polygon(linemerge(geom))
            except:
                is_first = True
                for LineString in geom: # Descarta polígonos que estão contidos dentro de outros
                    if is_first:
                        try:
                            geom = geometry.Polygon(LineString) 
                        except:
                            geom = LineString
                        is_first = False
                    try:
                        contained = geometry.Polygon(LineString)
                    except:
                        contained = LineString
                    if not geom.contains(contained):
                        geom = contained           
        else:
            geom = geometry.Polygon(geom)
        return geom
    
    def get_places(self, place_name,key,value,tags=("name","geom")):
        
        result = self._get_places_overpy(place_name,key,value) # demora!!!
        
        df = pd.DataFrame(columns=tags)

        #Verifica os resultados de cada tipo de geometria
        
        for n in result.nodes: 
            line = []     
            if n.tags.get("aeroway",np.nan) is not np.nan:   
                for t in tags:
                    if t != "geom":
                        line.append(n.tags.get(t, np.nan))
                    else:
                        line.append(geometry.Point([n.lon, n.lat]))

                df = df.append(pd.DataFrame([line],columns=tags))

        for w in result.ways:
            line = []
            if w.tags.get("name",np.nan) is not np.nan:

                for t in tags:
                    if t != "geom":
                        line.append(w.tags.get(t, np.nan))
                    else:
                        line.append(geometry.Polygon([[p.lon, p.lat] for p in w.get_nodes(resolve_missing=True)]))

                df = df.append(pd.DataFrame([line],columns=tags))


        for r in result.relations:

            line = []
            for t in tags:
                if t != "geom":
                    line.append(r.tags.get(t, np.nan))
            geom = geometry.LineString()
            cont = 0
            for m in r.members:
                coords = []
                if m.geometry and (m.role == "outer" or m.role == ""):
                    for p in m.geometry:           
                        coords.append([p.lon, p.lat])
                    cont+=1
                    
                geom = geom.union(geometry.LineString(coords))

            line.append(self._to_polygon(geom,cont))
            df = df.append(pd.DataFrame([line],columns=tags))
        
        df["key"] = key
        df["value"] = value
        return df.reset_index(drop=True)  