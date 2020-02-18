import json 

def parse_local(data):
  data_json = {}

  for local in data:
    data_json["name"] = local["properties"]["name"]
    data_json["key"] = local["properties"]["key"]
    data_json["value"] = local["properties"]["value"]
    
    location_json = {}
    location_json["type"] = str(local["geometry"]["type"]).lower()
    location_json["coordinates"] = local["geometry"]["coordinates"]

    data_json["location"] = location_json
    
    yield data_json

if __name__ == "__main__":
  print(parse_local("./data/test.json"))