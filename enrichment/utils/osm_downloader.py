from geopy.geocoders import Nominatim
from shapely.ops import polygonize
from shapely import geometry
import shapely.wkt
import pandas as pd
import numpy as np
import geopandas
import overpy
import folium
from shapely.ops import linemerge
import requests
import json

class OSM_util():        
    
    #Realiza a consulta coletando os três tipos de geometria (Node, Way e Relation) já setando a saída como JSON.
    @staticmethod
    def get_places_overpy(key, value, place_name):    
        api = overpy.Overpass()
        result = api.query("""
            [out:json][timeout:3600];
            {{geocodeArea: %s}}->.searchArea;
            (
              node[%s=%s](area.searchArea);
              way[%s=%s](area.searchArea);
              relation[%s=%s](area.searchArea);
            );
            out geom;
            >;
            out skel qt;
            """ % (place_name, key, value, key, value, key, value))
        return result
    
    #Corrige polígonos que são formados por vários polígonos 
    @staticmethod
    def to_polygon(geom, geom_size):
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
    
    @staticmethod
    def get_places(key, value, place_name, tags=("name","geom")):
        
        result = self.get_places_overpy(place_name, key, value) # demora!!!
        
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
                        print(w.tags.get("name",np.nan))
                        print(w.tags.get("name",np.nan))
                        line.append(geometry.Polygon([[p.lon, p.lat] for p in w.nodes]))

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

            line.append(self.to_polygon(geom,cont))
            df = df.append(pd.DataFrame([line],columns=tags))
        
        df["key"] = key
        df["value"] = value
        return df.reset_index(drop=True)     