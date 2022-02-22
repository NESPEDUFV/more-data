from elasticsearch.client.ingest import IngestClient
from ...utils import load_json


class PipelineHandler:
    """
    PipelineHandler create json object for elasticsearch pipeline.

    Parameters
    ----------
    description: str
        explain what is pipeline.
    target_field_name: str
        field name that will post the result of enrichment.
    match_field: str
        what index lookup field to bind the enrichments.
    policy_name: str
        name of policy.
    field_array: str
        name of field if the field you want to enrich is an array.
    max_matches: int
        if the matches is > 1 the target_field will be an array and
        the results of enrichments will bind more than 1 object to get result.
    shape_relation: str
        if the enrichment is geobased you have to put this parameter to specify
        which relation you want to get.

        - INTERSECTS
            Return all documents whose field intersects the query geometry.
        - DISJOINT
            Return all documents whose field has nothing in common with the query geometry.
        - WITHIN
            Return all documents whose field is within the query geometry.
        - CONTAINS
            Return all documents whose field contains the query geometry.

    Attributes
    ----------

    json: dict
        this attribute is the json created with the parameters specifying the pipeline.
    """

    def __init__(
        self, description, target_field_name, match_field, policy_name, **kwargs
    ):

        if kwargs.get("field_array"):
            self._json = {
                "description": description,
                "processors": [
                    {
                        "foreach": {
                            "field": kwargs.get("field_array"),
                            "processor": {
                                "enrich": {
                                    "policy_name": policy_name,
                                    "field": "_ingest._value." + match_field,
                                    "target_field": "_ingest._value."
                                    + target_field_name,
                                    "ignore_missing": True,
                                }
                            },
                            "ignore_failure": True,
                        }
                    }
                ],
            }

            if kwargs.get("remove_field"):
                remove_processor = {
                    "foreach": {
                        "field": kwargs.get("field_array"),
                        "processor": {
                            "remove": {
                                "field": "_ingest._value." + kwargs.get("remove_field"),
                                "ignore_missing": True,
                            }
                        },
                        "ignore_failure": True,
                    }
                }
                self._json["processors"].append(remove_processor)

            if kwargs.get("max_matches"):
                self._json["processors"][0]["foreach"]["processor"]["enrich"][
                    "max_matches"
                ] = kwargs.get("max_matches")

            if kwargs.get("shape_relation"):
                self._json["processors"][0]["foreach"]["processor"]["enrich"][
                    "shape_relation"
                ] = kwargs.get("shape_relation")
        else:
            self._json = {
                "description": description,
                "processors": [
                    {
                        "enrich": {
                            "policy_name": policy_name,
                            "field": match_field,
                            "target_field": target_field_name,
                            "ignore_missing": True,
                        }
                    }
                ],
            }

            if kwargs.get("remove_field"):
                remove_processor = {
                    "remove": {
                        "field": kwargs.get("remove_field"),
                        "ignore_missing": True,
                    }
                }

                self._json["processors"].append(remove_processor)

            if kwargs.get("max_matches"):
                self._json["processors"][0]["enrich"]["max_matches"] = kwargs.get(
                    "max_matches"
                )

            if kwargs.get("shape_relation"):
                self._json["processors"][0]["enrich"]["shape_relation"] = kwargs.get(
                    "shape_relation"
                )

    def import_json(self, data):
        pass

    def export_json(self):
        pass


class Pipeline:
    """
    A pipeline is a definition of a series of processors that
    are to be executed in the same order as they are declared.
    (https://www.elastic.co/guide/en/elasticsearch/reference/current/pipeline.html)

    Parameters
    ----------

    client: elasticsearch.Elasticsearch
        a elasticsearch client.
    name: str
        name for pipeline.
    pipeline_handler: :obj:`PipelineHandler`
        object that contains json object of pipeline.

    Attributes
    ----------

    client: str
    name: str
    pipeline_handler: :obj:`PipelineHandler`
    """

    def __init__(self, client, name, pipeline_handler):
        self._pipeline_handler = pipeline_handler
        self._name = name
        self.ingest_client = IngestClient(client)

    def create_pipeline(self, params=None):
        """
        create_pipeline method create the elasticsearch pipeline
        with processors specified in pipeline_handler json.
        """
        try:
            self.ingest_client.put_pipeline(
                self._name, load_json(self._pipeline_handler._json)
            )
        except Exception as e:
            raise (e)
