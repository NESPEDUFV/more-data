import json 
import csv
from h3 import h3

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

def __POI_parser(point):
  point["code_h3"] = h3.geo_to_h3(point["latitude"], point["longitude"], 8)
  return point

def parse_local_geojson(data):
  # TODO: copy the style of user's yield parser

  data_json = {}

  for local in data:
    data_json["name"] = local["properties"]["name"]
    data_json["key"] = local["properties"]["key"]
    data_json["value"] = local["properties"]["value"]
    
    location_json = {}
    location_json["type"] = str(local["geometry"]["type"]).lower()
    location_json["coordinates"] = local["geometry"]["coordinates"]

    data_json["location"] = location_json
    
    yield data_json["features"]

def csv_generator(data):
  with open(data, "r") as f:
    reader = csv.DictReader(f)
    for cnt, row in enumerate(reader):
      yield row

def parse_setores(data):
  with open(data, "r") as f:
    reader = csv.DictReader(f)
    for cnt, row in enumerate(reader):
      yield {
        "setor_id": row["0"],
        "code": row["1"]
      }
      
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