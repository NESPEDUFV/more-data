import json
import csv
from h3 import h3
from ..utils import read_json_from_file, load_json
from shapely.geometry import asPoint
from numpy import array


def _add_geo_location(doc):
    doc["geo_location"] = asPoint(array([doc["longitude"], doc["latitude"]])).wkt
    return doc


def _add_code_point(doc):
    doc["code_h3"] = h3.geo_to_h3(doc["latitude"], doc["longitude"], 8)
    return doc


def parse_document(data, **kwargs):
    array_point_field = kwargs.get("array_point_field")
    geo_location = kwargs.get("geo_location")
    code_h3 = kwargs.get("code_h3")

    for doc in read_json_from_file(data):
        if geo_location:
            if array_point_field is not None:
                doc[array_point_field] = [
                    _add_geo_location(points) for points in doc[array_point_field]
                ]
            else:
                doc = _add_geo_location(doc)

        if code_h3:
            if array_point_field is not None:
                doc[array_point_field] = [
                    _add_code_point(points) for points in doc[array_point_field]
                ]
            else:
                doc = _add_code_point(doc)
        yield doc
