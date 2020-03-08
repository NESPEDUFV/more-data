import json

from elasticsearch import Elasticsearch

import models
import time

HOST = 'localhost'
PORT = 9200

PIPELINE_DIR = "../elk-maps/pipelines/"
ENRICH_DIR = "../elk-maps/enriches/"

APP_POLICY_FILE = ENRICH_DIR + "app-user-policy.json"
SECTOR_POLICY_FILE = ENRICH_DIR + "sectors-policy.json"
CENSUS_POLICY_FILE = ENRICH_DIR + "census-policy.json"

USER_PIPELINE = PIPELINE_DIR + "user-pipeline.json"
CENSUS_PIPELINE = PIPELINE_DIR + "census-pipeline.json"
SECTORS_PIPELINE = PIPELINE_DIR + "sectors-pipeline.json"

def read_json(file):
  with open(file, "r") as f:
    return json.loads(f.read())

def __user_enricher():
  policies = [
      {
        "name": "app-user-policy",
        "file": APP_POLICY_FILE
      },
      {
        "name": "sector-policy",
        "file": SECTOR_POLICY_FILE
      },
      {
        "name": "census-policy",
        "file": CENSUS_POLICY_FILE
      }
    ] 
  for policy in policies:
    mapping = read_json(policy["file"])
    enricher = models.Enricher(es, mapping, policy["name"]) 

    enricher.create_policy()
    enricher.execute_policy()
  
  pipe = models.pipeline.Pipeline(es, "user-lookup", USER_PIPELINE)
  pipe.create_pipeline() 

def __create_census_pipeline():
  json = read_json(CENSUS_PIPELINE)
  pipe = models.pipeline.Pipeline(es, "census-pipeline", json)
  pipe.create_pipeline() 

def __create_sectors_pipeline():
  json = read_json(SECTORS_PIPELINE)
  pipe = models.pipeline.Pipeline(es, "sectors-pipeline", json)
  pipe.create_pipeline() 

if __name__ == "__main__":
  es = Elasticsearch(
    hosts=[{'host': HOST, 'port': PORT}],
    timeout = 10000
  )  

  # __create_census_pipeline()
  # __create_sectors_pipeline()
  __user_enricher()

  
  # es.update_by_query(body=None, index="users", pipeline="app-user-lookup")
  # TODO: increase the read_timeout or change method of update_by_query
  # HINT: reindex document with pipeline



