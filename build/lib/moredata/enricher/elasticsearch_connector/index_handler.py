import json
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk, reindex, scan
from elasticsearch.helpers.errors import BulkIndexError


class IndexHandler:
    """Index Handler control index actions in Elasticsearch.

    Parameters
    ----------
    client: :obj:`elasticsearch.Elasticsearch`
    index: str
        name of index
    doc_type: str
        name of document

    Attributes
    ----------
    client: :obj:`elasticsearch.Elasticsearch`
    index: str
        name of index
    doc_type: str
        name of document
    """

    def __init__(self, client, index, doc_type):
        self.client = client
        self.index = index
        self.doc_type = doc_type

    def create_index(self, mapping):
        """This method create index with mapping provided using
        elasticsearch-py package (https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.client.IndicesClient.create)

        Parameters
        ----------
        mapping: :obj:`Json`
            mapping is a definitions of attributes index types (https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)
        """
        try:
            self.client.indices.create(index=self.index, body=mapping)
        except TransportError as e:
            if e.error == "resource_already_exists_exception":
                pass
            else:
                raise

    def load_index(self, parser, streaming=None, **kwargs):
        """load_index method load documents to specified index in constructor.
        It can stream the load or just load all data passing an `iterable` as parameter.
        The difference between of these two methods is that if you want that your data assume specified
        type you have to stream but if you don't care about this you can simply bulk data that
        elasticsearch will infer the types of your document.

        Parameters
        ----------
        pasrser: Callable
            It's a function that yield the document which has data to index into elasticsearch.

        streaming: bool
            If streaming load_index method will do streaming bulk instead of bulk all data.
        """
        try:
            if streaming:
                for ok, _ in streaming_bulk(
                    self.client, index=self.index, actions=parser(**kwargs)
                ):
                    if not ok:
                        raise Exception
            else:
                bulk(
                    self.client,
                    parser(**kwargs),
                    index=self.index,
                    doc_type=self.doc_type,
                )
        except BulkIndexError as e:
            pass

    def _remove_fields_preprocessed(self, data, **kwargs):
        array_point_field = kwargs.get("array_point_field")
        geo_location = kwargs.get("geo_location")
        code_h3 = kwargs.get("code_h3")

        if geo_location:
            if array_point_field:
                for points in data[array_point_field]:
                    points = points.pop("geo_location", None)
            else:
                data = data.pop("geo_location", None)

        if code_h3:
            if array_point_field:
                for points in data[array_point_field]:
                    points = points.pop("code_h3", None)
            else:
                data = data.pop("code_h3", None)

        return data

    def get_all_data(self, index, **kwargs):
        """Get all data indexed by a index.

        Parameters
        ----------
        index: str
            name of index

        query: dict
            query is the document that elasticsearch uses to retrive information

        Yields
        ------
        generate the data retrieved by elasticsearch.

        """

        query = {"query": {"match_all": {}}}

        for record in scan(self.client, query=query, index=index):
            if kwargs.get("geo_location") or kwargs.get("code_h3"):
                yield self._remove_fields_preprocessed(record["_source"], **kwargs)
            else:
                yield record["_source"]

    def re_index(self, reindex_handler):
        """reindex to apply pipeline to enrich

        Parameters
        ----------
        reindex_handler: :obj:`ReindexHandler`
        """
        self.client.reindex(reindex_handler._json)


class ReindexHandler:
    """ReindexHandler creates a necessary json to send to elasticsearch to reindex with pipeline
    and enrich the index provided.

    Parameters
    ----------
    index: str
        name of source index

    target_index: str
        name of destination index

    pipeline_name: str
        name of pipeline


    Attributes
    ----------

    json: dict
        this is a json file created by the parameters to sendo to reindex route
    """

    def __init__(self, index, target_index, pipeline_name):
        self._json = {
            "source": {"index": index},
            "dest": {"index": target_index, "pipeline": pipeline_name},
        }

        self.source_index = index
        self.target_index = target_index
