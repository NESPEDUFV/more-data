import csv

class Parser:
  def __init__(self, data_dir, data_type):
    self.data_dir = data_dir
    self.data_type = data_type
  
  def parser_csv(self):
    with open(data_dir) as f:
      reader = csv.DictReader(f)
      yield reader
  
  def parse_local_geojson():
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
  
  def parse_user(): 
    #TODO: Add a kwargs of read function to make optional arg for parser functions
  
    for user in data:
      user['external_identifier'] = str(user['external_identifier'])

      if(user['external_identifier'] != 'true' 
        and user['external_identifier'] != "false" 
        and user['external_identifier'] != ""):
        yield {
          "external_identifier": str(user['external_identifier']),
          "operating_system": user['operating_system'],
          "user_segments_id_list": user['user_segments_id_list'],
          "radius_gyration": user['radius_of_gyration'],
          "last_handset": user['last_handset'],
          "last_network_operator": user['last_network_operator'],
          "points_of_interest": [points for points in user['points_of_interest']],
          "host_app_frequency": user['host_app_frequency'],
          "job_reference_date": user['job_reference_date']
        }