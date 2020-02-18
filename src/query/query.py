import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

host = 'localhost'
path_user_json_input = '../data/json/user_profile_17092019.json'
query_path = 'app.json'

def create_user_index(client, index):
    app_mapping = {
      "properties": {
        "#id": {
          "type": "long"
        },
        "android_id": {
          "type": "long"
        },
        "app_name": {
          "type": "text"
        },
        "package_name": {
          "type": "text"
        },
        "content_rating": {
          "type": "text"
        },
        "reviews_score": {
          "type": "double"
        },
        "reviews_counter": {
          "type": "long"
        },
        "installations_counter": {
          "type": "text"
        },
        "category": {
          "type": "text"
        }, 
        "overall_value_category": {
          "type": "double"
        },
        "rank_category": {
          "type": "double"
        }
      }
    }

    user_mapping = {
      "mappings": {
        "properties": {
          "external_identifier": {
            "type": "text"
          },
          "app": app_mapping,
          "operating_system": {
            "type": "text"
          },
          "user_segments_id_list": {
            "type": "long"
          },
          "radius_gyration": {
            "type": "nested",
            "properties": {
              "centroid_location": {
                "type": "geo_point"
              },
              "radius": {
                "type": "double"
              }
            }
          },
          "last_handset": {
            "type": "nested",
            "properties": {
              "handset_code": {
                "type": "text"
              },
              "installations_number": {
                "type": "long"
              }
            }
          },
          "last_network_operator": {
            "type": "text"
          },
          "points_of_interest": {
            "type": "nested",
            "properties": {
              "location": {
                "type": "geo_point"
              },
              "type": {
                "type": "text"
              },
              "radius": {
                "type": "long"
              }
            }
          },
          "host_app_frequency": {
            "type": "text"
          },
          "job_reference_date": {
            "type": "date"
          }
        }
      }
    }

    # create empty index
    try:
        client.indices.create(index=index, body=user_mapping)
    except TransportError as e:
        # ignore already existing index
        if e.error == "resource_already_exists_exception":
            pass
        else:
            raise

def parse_user(data):
  for user in data:
      dict_query = { "query": { "terms": { "#id": user['applications_id_list'] } } }
      query = json.loads(json.dumps(dict_query))
      res = es.search(index="apps", body=query)

      user['external_identifier'] = str(user['external_identifier'])

      if(user['external_identifier'] != 'true' 
        and user['external_identifier'] != "false" 
        and user['external_identifier'] != ""):
        yield {
          "external_identifier": str(user['external_identifier']),
          "app": [apps["_source"] for apps in res['hits']['hits']],
          "operating_system": user['operating_system'],
          "user_segments_id_list": user['user_segments_id_list'],
          "radius_gyration": user['radius_of_gyration'],
          "last_handset": user['last_handset'],
          "last_network_operator": user['last_network_operator'],
          "points_of_interest": [points for points in user['points_of_interest']],
          "host_app_frequency": user['host_app_frequency'],
          "job_reference_date": user['job_reference_date']
        }

def load_user(client, data, index="users"):
  create_user_index(client, index)

  for ok, result in streaming_bulk(
        client,
        parse_user(data),
        index=index,
        chunk_size=500
    ):
        action, result = result.popitem()
        doc_id = "/%s/doc/%s" % (index, result["_id"])
        
        if not ok:
            print("Failed to %s document %s: %r" % (action, doc_id, result))
        else:
            print(doc_id)

def bulk_es_chunks(len, es, data):
  for i in range(1, int(len / 502)):
    if i == 1:
      start = i
      end = i * 500
    else : 
      start = end+1
      end += i * 500

    load_user(es, data[start-1 : end])


if __name__ == '__main__':
  es = Elasticsearch(
    hosts=[{'host': host, 'port': 9200}]
  )

  with open(path_user_json_input, 'r') as datafile:
    data = json.loads(datafile.read())

  bulk_es_chunks(52000, es, data) # 52000 is a length greater than the length of json for finish the process of bulk_es_chunks
