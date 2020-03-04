import json 

def get_lat_long(user):
    lat_long = []
    for points_of_interest in user["points_of_interest"]:
        dict = {"latitude": points_of_interest["latitude"], 
        "longitude": points_of_interest["longitude"]}
        
        lat_long.append(dict)

    return lat_long

def get_query_locals_user(lat_long_list):
    locals_query = [] 
    for lat_long_dict in lat_long_list:
      dict_shape = {}
      dict_location = {}
      dict_geo_shape = {}
      dict_filter = {}

      coord = []
      coord.append(lat_long_dict["latitude"])
      coord.append(lat_long_dict["longitude"])

      dict_shape["type"] = "point"
      dict_shape["coordinates"] = coord

      dict_location["shape"] = dict_shape
      dict_location["relation"] = "contains"

      dict_geo_shape["location"] = dict_location

      dict_filter["geo_shape"] = dict_geo_shape

      locals_query.append(dict_filter)


    query = {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
        "filter": locals_query
    }

    return json.loads(json.dumps(query))

# def get_user_elastic_json_data(data_path):
#     user_profile_data = read_json_elasticsearch(data_path)
#     for user in user_profile_data:
#       user = user["_source"]
#       lat_long_user = get_lat_long(user)
#       setores_user = {"": get_setores_of_user(lat_long_user) }
#       user.update(setores_user)

#     write_json(user_profile_data, data_path)