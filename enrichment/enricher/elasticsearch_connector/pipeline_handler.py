from elasticsearch.client.ingest import IngestClient
import utils.util as util

class PipelineHandler():
    #Refactorate

    def __init__(self, description, target_field_name, match_field, policy_name, **kwargs):
        # think about create decorator 

        if kwargs.get('field_array'):
            self._json = {
                "description" : description,
                "processors": [
                    {
                        "foreach":{
                            "field": kwargs.get('field_array'),
                            "processor": {
                                "enrich": {
                                    "policy_name": policy_name,
                                    "field": "_ingest._value."+match_field,
                                    "target_field": "_ingest._value."+target_field_name,
                                }
                            },
                            "ignore_failure": True
                        }
                    }
                ]
            }
        
            if kwargs.get('max_matches'):
                self._json['processors'][0]['foreach']["processor"]['enrich']['max_matches'] = kwargs.get('max_matches')
            
            if kwargs.get('shape_relation'):
                self._json['processors'][0]['foreach']['processor']['enrich']['shape_relation'] = kwargs.get('shape_relation')

        else:
            self._json = {
                "description": description,
                "processors": [
                    {
                        "enrich": {
                            "policy_name": policy_name,
                            "field": match_field,
                            "target_field": target_field_name,
                        }
                    }
                ]
            }

            if kwargs.get('max_matches'):
                self._json['processors'][0]['enrich']['max_matches'] = kwargs.get('max_matches')
            
            if kwargs.get('shape_relation'):
                self._json['processors'][0]['enrich']['shape_relation'] = kwargs.get('shape_relation')
    
    def import_json(self, data):
        pass

    def export_json(self):
        pass

class Pipeline:

    def __init__(self, client, name, pipeline_handler):
        """
          Parameters
          ----------
          client: a elasticsearch client
          id: name for pipeline
          pipeline: file of pipeline
        """

        self._pipeline_handler = pipeline_handler
        self._name = name
        self.ingest_client = IngestClient(client)

    def create_pipeline(self, params=None):
        try:
            self.ingest_client.put_pipeline(self._name, util.load_json(self._pipeline_handler._json))
        except Exception as e:
            raise(e)
