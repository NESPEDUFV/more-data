# this is a old version of enrichment 
# need refactoring
# TODO: refactorate
import json
from h3 import h3
import dask.dataframe as dd
import dask
import pandas as pd
import multiprocessing

df_setores = dd.read_csv(r'../../datasets/setores/*.csv')
df_setores = df_setores.rename(columns={'Unnamed: 0': 'id', '0': 'setor_id', '1': 'code'})

df_census = pd.read_csv(r'../../datasets/df_census_2010.csv')
df_census.rename(columns = {"Cod_setor": "setor_id"}, inplace=True)

def write_json(data, filename): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=2) 

def read_json_elk(path):
    with open(path, 'r') as reader:
        str = "[" + reader.read()
        str = str.replace("\n", ",\n")
        str = str + "]" 
        return json.loads(json.dumps(str))

def search_setor_id(lat, long):
    code = h3.geo_to_h3(lat, long, 8)
    setor_id = df_setores[df_setores["code"]==code]
    return setor_id.compute()

def get_lat_long(user):
    lat_long = []
    for points_of_interest in user["points_of_interest"]:
        dict = {"latitude": points_of_interest["latitude"], 
        "longitude": points_of_interest["longitude"]}
        
        lat_long.append(dict)

    return lat_long

def get_setores_of_user(lat_long_list):
    setores = []
    for lat_long_dict in lat_long_list:
        print(lat_long_dict["latitude"], lat_long_dict["longitude"])
        
        import time
        start = time.time()
        df_setor_id = search_setor_id(lat_long_dict["latitude"], lat_long_dict["longitude"])
        end = time.time()
        print(end-start)
    
        ddf_result = dd.merge(df_setor_id, df_census, on="setor_id", how="inner")
        
        if not ddf_result.empty: 
            arr_values = ddf_result.values[0]
            columns_census = df_census.columns

            dict_census_user = {columns_census[i]: arr_values[i] for i in range(len(columns_census))} 

            setor = list(filter(lambda setor: setor["setor_id"] == dict_census_user["setor_id"], setores))
            print(setor)

            if not setor:
                setores.append(dict_census_user)
    
    return setores

def parsing_elk_data(user_profile_data):    
    with open(user_profile_data, 'r') as json_file:
        for user in json.loads(json_file.read()):
            user = user["_source"]
            lat_long_user = get_lat_long(user)
            setores_user = {"setores": get_setores_of_user(lat_long_user) }
            user.update(setores_user)

        write_json(user_profile_data, data_path)

if __name__ == '__main__':
    parsing_elk_data("test.json")
    
def test():
    parsing_elk_data("test.json")


