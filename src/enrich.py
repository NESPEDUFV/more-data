import json

from elasticsearch import Elasticsearch

import models
import time

HOST = 'localhost'
PORT = 9200

POLICY_FILE = "../enriches/app-id-policy.json"
POLICY_PIPELINE = "../pipelines/app-id-pipeline.json"

def read_json(file):
  with open(file, "r") as f:
    return json.loads(f.read())


if __name__ == "__main__":
  es = Elasticsearch(
    hosts=[{'host': HOST, 'port': PORT}],
    timeout=40
  )  

  #enrich user document
  policy = read_json(POLICY_FILE)
  pipeline = read_json(POLICY_PIPELINE)
  
  enricher = models.Enricher(es, "app-user-lookup", policy, "app-user-policy", pipeline) 

  enricher.create_policy()
  enricher.execute_policy()
  enricher.create_pipeline()

  es.update_by_query(body=None, index="users", pipeline="app-user-lookup")
  # TODO: increase the read_timeout or change method of update_by_query
  # HINT: reinddex document with pipeline



