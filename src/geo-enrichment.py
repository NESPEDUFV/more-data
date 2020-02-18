from shapely import wkt
import geopandas as gpd
import pandas as pd
import numpy as np

def get_geo_dataframe(filename, column):
  df = pd.read_csv(filename)
  df[column] = df[column].apply(wkt.loads)

  gdf = gpd.GeoDataFrame(df, geometry=column)
  return gdf

def write_geo_json(gdf, filename):
  gdf.to_file("./data/"+filename, driver='GeoJSON')

def parse_geodf_geoJSON_from_path(path, column):
  import os

  for filename in os.listdir(path):
    print(path+filename)
    gdf = get_geo_dataframe(path+filename, column)
    write_geo_json(gdf, filename[:len(filename)-4]+".geojson")

def parse_geodf_geoJSON_from_file(filename, column):
  gdf = get_geo_dataframe(filename, column)
  write_geo_json(gdf, filename[:len(filename)-4]+".geojson")

if __name__ == "__main__":
  # write_geo_json(get_geo_dataframe("../Locais_OSM/aeroway_aerodrome.csv"), "aeroway_aerodrome.geojson")
  parse_geodf_geoJSON_from_path("../Locais_OSM/", "geom")
