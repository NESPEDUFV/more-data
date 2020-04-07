import json
import csv
from h3 import h3
from ..utils.util import read_json_from_file
from shapely.geometry import asPoint
from numpy import array


def __read_unstructured_json(data):
    with open(data, "r") as f:
        str = "[" + f.read()
        str = str.replace("\\", "")
        str = str.replace('''"{''', '{')
        str = str.replace('''}"''', '}')
        str = str.replace('''"[''', '[')
        str = str.replace(''']"''', ']')
        str = str.replace('''""''', '''"''')
        str = str.replace(''':",''', ''':"",''')
        str = str.replace("\n", ",\n")
        str = str + "]"
        return json.loads(json.dumps(str))


def csv_generator(data):
    csv.field_size_limit(2147483647)
    with open(data, "r") as f:
        reader = csv.DictReader(f)
        for cnt, row in enumerate(reader):
            yield row


def __add_geo_location(doc):
    doc["geo_location"] = asPoint(array([doc["longitude"], doc["latitude"]])).wkt
    return doc

def __add_code_point(doc):
    doc["code_h3"] = h3.geo_to_h3(doc["latitude"], doc["longitude"], 8)
    return doc


def parse_local_geojson(data):
    data = read_json_from_file(data)
    for local in data["features"]:
        if (local["properties"]["name"] != "null" and local["geometry"]["type"] != "Point"):
            yield {
                "name": local["properties"]["name"],
                "key": local["properties"]["key"],
                "value": local["properties"]["value"],
                "location": {
                    "type": str(local["geometry"]["type"]).lower(),
                    "coordinates": local["geometry"]["coordinates"]
                }
            }


def parse_census(data):
    with open(data, "r") as f:
        reader = csv.DictReader(f)
        for cnt, row in enumerate(reader):
            cod = str(row["Cod_setor"])
            row["Cod_setor"] = cod[:len(cod)-2]
            yield row


def parse_setores(data):
    with open(data, "r") as f:
        reader = csv.DictReader(f)
        for cnt, row in enumerate(reader):
            yield {
                "setor_id": row["0"],
                "code": row["1"]
            }


def parse_document(data, **kwargs):
    array_point_field = kwargs.get('array_point_field')
    geo_location = kwargs.get('geo_location')
    code_h3 = kwargs.get('code_h3')

    for doc in json.loads(__read_unstructured_json(data)):
        if geo_location:
            if array_point_field != None:
                doc[array_point_field] = [__add_geo_location(points) for points in doc[array_point_field]]
            else:
                doc = __add_geo_location(doc)
        
        if code_h3:
            if array_point_field != None:
                doc[array_point_field] = [__add_code_point(points) for points in doc[array_point_field]]
            else:
                doc = __add_code_point(doc)
        yield doc

def parse_user(data):
    for user in json.loads(__read_unstructured_json(data)):
        user['external_identifier'] = str(user['external_identifier'])

        if(user['external_identifier'] != 'true'
                and user['external_identifier'] != "false"
                and user['external_identifier'] != ""):
            yield {
                "external_identifier": str(user['external_identifier']),
                "applications_id_list": [str(id)+".0" for id in user['applications_id_list']],
                "operating_system": user['operating_system'],
                "user_segments_id_list": user['user_segments_id_list'],
                "radius_gyration": user['radius_of_gyration'],
                "last_handset": user['last_handset'],
                "last_network_operator": user['last_network_operator'],
                "points_of_interest": [__POI_parser(points) for points in user['points_of_interest']],
                "host_app_frequency": user['host_app_frequency'],
                "job_reference_date": user['job_reference_date']
            }