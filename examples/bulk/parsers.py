import simplejson as json
import csv

def read_json_from_file(file):
	with open(file, "r") as f:
		return json.loads(f.read())


def load_json(json_object):
	return json.loads(json.dumps(json_object))

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


def csv_generator(data):
    csv.field_size_limit(2147483647)
    with open(data, "r") as f:
        reader = csv.DictReader(f)
        for cnt, row in enumerate(reader):
            yield row