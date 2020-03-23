import json
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk, reindex
from elasticsearch.helpers.errors import BulkIndexError


class IndexHandler:
    def __init__(self, client, index, doc_type):
        self.client = client
        self.index = index
        self.doc_type = doc_type
        

    def create_index(self, mapping):
        try:
            self.client.indices.create(index=self.index, body=mapping)
        except TransportError as e:
            if e.error == "resource_already_exists_exception":
                pass
            else:
                raise


    def load_index(self, parser, streaming=None):
        try:
            if streaming:
                for ok, response in streaming_bulk(self.client, index=self.index, actions=parser()):
                    if not ok:
                        # failure inserting
                        print(response)
                else:
                    bulk(
                        self.client,
                        parser(),
                        index=self.index,
                        doc_type=self.doc_type
                    )
        except BulkIndexError as e:
            pass


    def get_all_data(self, index, query):
        res = scan(self.client,
            query=query,
            index=index)
        
        for data in res["_source"]:
            yield data


    def reindex(self, reindex_handler):
        reindex(self.client, reindex_handler._json)


class ReindexHandler:
    def __init__(self, index, target_index, pipeline_name):
        self._json = {
            "source": {
                "index": index
            },
            "dest": {
                "index": target_index,
                "pipeline": pipeline_name
            }
        }
