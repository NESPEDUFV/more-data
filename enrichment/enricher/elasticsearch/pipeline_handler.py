from elasticsearch.client.ingest import IngestClient


class Pipeline:

    def __init__(self, client, id, pipeline):
        """
          Parameters
          ----------
          client: a elasticsearch client
          id: name for pipeline
          pipeline: file of pipeline
        """

        self.pipeline = pipeline
        self.id = id
        self.ingest_client = IngestClient(client)

    def create_pipeline(self, params=None):
        try:
            self.ingest_client.put_pipeline(self.id, self.pipeline)
        except Exception as e:
            raise(e)


class PipelineEnrichHandler(Pipeline):

    def __init__(self, client, name_pipeline, description, target_field_name, match_field, policy_name, match_field_array=None, max_matches=None):
        # think about create decorator :)
        """
             Parameters
             ----------
             client: a elasticsearch client
             id: name for pipeline
             pipeline: ingest pipeline
           """

        pipeline_json = {
            "description": "Enriching app details to user",
            "processors": [
                {
                    "enrich": {
                        "policy_name": policy_name,
                        "field": match_field,
                        "target_field": target_field_name,
                        "max_matches": 128
                    }
                }
            ]
        }

        if

        super(PipelineHandler, self).__init__(client, id)

