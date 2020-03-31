from shapely import wkt
import geopandas as gpd
import pandas as pd
import numpy as np

def __get_geo_dataframe(filename, column):
  df = pd.read_csv(filename)
  df[column] = df[column].apply(wkt.loads)

  gdf = gpd.GeoDataFrame(df, geometry=column)
  return gdf

def __write_geo_json(gdf, filename):
  gdf.to_file(filename, driver='GeoJSON')

def parse_geodf_geoJSON_from_path(path, column):
  import os

  for filename in os.listdir(path):
    print(path+filename)
    gdf = __get_geo_dataframe(path+filename, column)
    __write_geo_json(gdf, filename[:len(filename)-4]+".geojson")

def parse_geodf_geoJSON_from_file(filename, column):
  gdf = __get_geo_dataframe(filename, column)
  __write_geo_json(gdf, filename[:len(filename)-4]+".geojson")
