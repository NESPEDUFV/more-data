import json

from elasticsearch import Elasticsearch

import enrichment.models as models

import time

HOST = 'localhost'
PORT = 9200

PIPELINE_DIR = "../elk-maps/pipelines/"
ENRICH_DIR = "../elk-maps/enriches/"

APP_POLICY_FILE = ENRICH_DIR + "app-user-policy.json"
SECTOR_POLICY_FILE = ENRICH_DIR + "sectors-policy.json"
CENSUS_POLICY_FILE = ENRICH_DIR + "census-policy.json"
LOCALS_POLICY_FILE = ENRICH_DIR + "locals-policy.json"

USER_APP_PIPELINE = PIPELINE_DIR + "user-app-pipeline.json"
USER_CENSUS_PIPELINE = PIPELINE_DIR + "user-census-pipeline.json"
USER_SECTORS_PIPELINE = PIPELINE_DIR + "user-sectors-pipeline.json"
USER_LOCALS_PIPELINE = PIPELINE_DIR + "user-locals-pipeline.json"


def read_json(file):
    with open(file, "r") as f:
        return json.loads(f.read())


def __create_policies():
    policies = [
        {
            "name": "app-user-policy",
            "file": APP_POLICY_FILE
        },
        {
            "name": "census-policy",
            "file": CENSUS_POLICY_FILE
        },
        {
            "name": "sector-policy",
            "file": SECTOR_POLICY_FILE
        }
    ]
    for policy in policies:
        mapping = read_json(policy["file"])
        enricher = models.Enricher(es, mapping, policy["name"])

        enricher.create_policy()
        enricher.execute_policy()


def __create_pipelines():
    pipelines = [
        {
            "name": "user-census-pipeline",
            "file": USER_CENSUS_PIPELINE
        },
        {
            "name": "user-sectors-pipeline",
            "file": USER_SECTORS_PIPELINE
        },
        {
            "name": "user-app-pipeline",
            "file": USER_APP_PIPELINE
        }
    ]

    for pipe in pipelines:
        mapping = read_json(pipe["file"])
        pipeliner = models.Pipeline(es, pipe["name"], mapping)

        pipeliner.create_pipeline()


if __name__ == "__main__":
    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': PORT}],
        timeout = 10000
    )

    # __create_policies()
    # __create_pipelines()

    # from elasticsearch import TransportError
    # try:
    #   mapping = read_json(LOCALS_POLICY_FILE)
    #   enricher = models.Enricher(es, mapping, "locals-policy")
    #   enricher.create_policy()
    #   enricher.execute_policy()
    # except TransportError as e:
    #   print(e.info)


    mapping = read_json(USER_LOCALS_PIPELINE)
    pipeliner = models.Pipeline(es, "user-locals-pipeline", mapping)
    pipeliner.create_pipeline()

    # es.update_by_query(body=None, index="users", pipeline="app-user-lookup")
    # TODO: increase the read_timeout or change method of update_by_query
    # HINT: reindex document with pipeline
