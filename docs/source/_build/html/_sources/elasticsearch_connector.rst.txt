.. _elasticsearch_connector:


Elasticsearch Connector
=======================
Example
~~~~~~~

If you want to enrich with elasticsearch you have to provide a client to the enricher, 
and others classes 
:class:`~moredata.enricher.elasticsearch_connector.index_handler`, 
:class:`~moredata.enricher.elasticsearch_connetor.index_handler.reindex_handler`,
:class:`~moredata.enricher.elasticsearch_connector.pipeline_handler`,
:class:`~moredata.enricher.elasticsearch_connector.policy_handler`,
that enricher need.

Firstly, you have to insert your data into elasticsearch, so using ``index_handler``:

Here, you have created a Data with a function that parse your document, that function is a default, but you
can create your own parser function that implements some nice features for your enrichment. After that, you 
instantiate an ``index_handler`` and use load_index method, passing a parser and others kwargs. We will enrich a
specific `geo_location` enrichment so we need the `geo_location` and `code_h3` equals true. The `code_h3` is to get the point
and hashing this point using `h3 library <https://github.com/uber/h3>`_. If the lat/long is in array object you have to pass the name of this field.

.. code-block:: python
   
   from moredata.enricher import Enricher, EnricherBuilder
   from moredata.enricher.elasticsearch_connector import (
      ElasticsearchConnector, 
      IndexHandler,
      ReindexHandler, 
      Pipeline, 
      PipelineHandler, 
      PolicyHandler, 
      Policy,
   )
   from moredata.models.data import Data
   from moredata.parser import parse_document
   from moredata.utils.util import read_json_from_file

   from elasticsearch import Elasticsearch
   
   es = Elasticsearch(
      hosts=[{'host': HOST, 'port': PORT}],
      timeout = 10000
   )

   user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json", unstructured_data=True)
   index_handler = IndexHandler(client, "users", "user")
   index_handler.load_index(parser=data.parse, array_point_field="points_of_interest", geo_location=True, code_h3=True)


Here we have a `geo_location` enrichment based on latitude and longitude, and has a query with `CONTAINS`, 
so every point in `points_of_interest` will be enriched if this point is contained by a geo shape that is a field
defined by the policy of `city-policy`.

.. code-block:: python
   
   elk_city_enricher = Enricher(connector=ElasticsearchConnector(
                                 index_handler=IndexHandler(client=es, index="cities", doc_type="city"),
                                 pipeline=Pipeline(client=es,
                                                   name="user-city-enricher",
                                                   pipeline_handler=PipelineHandler(
                                                         description="enriching user with cities",
                                                         match_field="geo_location",
                                                         target_field_name="city",
                                                         policy_name="city-policy",
                                                         field_array="points_of_interest",
                                                         shape_relation="CONTAINS")),
                                 reindex_handler=ReindexHandler(index="users",
                                                                  target_index="users-city-enriched",
                                                                  pipeline_name="user-city-enricher")))

Here it's returning the result of enrichment to `user_enriched` variable without fields that are created 
in Enricher, `geo_location` and `code_h3`.

.. code-block:: python
   
   user_enriched = \
      EnricherBuilder(user) \
      .with_enrichment(elk_city_enricher) \
      .get_result(array_point_field="points_of_interest", geo_location=True, code_h3=True)

With the code below it's written the result of enrichment in two formats json or csv. This library supports three conversions file type: parquet, json and csv. You can see more about this here: :ref:`conversion`
It's up to developer choose what type of file it'll be written.

.. code-block:: python

   import moredata.utils.util as util
   util.write_json_generator_to_json("../../data/output/json/user-enriched", user_enriched, 1000) 
   util.Converter.json_enriched_to_csv("../../data/output/json/*.json", "../data/output/csv/")



Elasticsearch Connector
-----------------------

.. py:module:: moredata.enricher.elasticsearch_connector.elasticsearch_connector

.. autoclass:: ElasticsearchConnector 
    :members:


Index Handler
-------------

Example
~~~~~~~

With index handler we can insert data into elasticsearch. When you want to define your `mapping <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html>`_ you should send data with optional argument ``streaming`` equals `True`. If you don't know mapping of the data even so you can load data without that optional argument and elasticsearch will infer the types of your data. 

.. code-block:: python
    
    import moredata.parser as parser
    import moredata.models as models
    from moredata.enricher.elasticsearch_connector import IndexHandler
    from moredata.utils.util import read_json_from_file
    
    from elasticsearch import Elasticsearch

    es = Elasticsearch(
        hosts=[{'host': 'localhost', 'port': 9200}]
    )

    index_handler = IndexHandler(client, "apps-json", "app")

    mapping = read_json_from_file(MAPPING_APPS_FILE)
    index_handler.create_index(mapping=mapping)

    index_handler.load_index(parser=app.parse, streaming=True)  


.. py:module:: moredata.enricher.elasticsearch_connector.index_handler

.. autoclass:: IndexHandler
    :members:


Reindex Handler
---------------

To enrich data this library provide a high-level client for `reindex api <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html>`_.

Example
~~~~~~~

Here we have a json object that you can send to elasticsearch to reindex using a pipeline for enrich twitter data.

.. code-block:: json
    
    {
        "source": {
            "index": "twitter"
        },
        "dest": {
            "index": "new_twitter",
            "pipeline": "enricher"
        }
    }

Simplifying this json object we can use.

.. code-block:: python

    ReindexHandler(index="twitter", target_index="new_twitter", pipeline_name="enricher")

.. warning::
    The pipeline referenced by ``pipeline_name`` in reindex object should already be created likewise the indexes.

.. autoclass:: ReindexHandler
    :members:


Pipeline
--------

Pipeline with Pipeline Handler controls what and which fields will be enriched by the elasticsearch. 
`Pipeline Documentation <https://www.elastic.co/guide/en/elasticsearch/reference/current/pipeline.html>`_

Example
~~~~~~~

This pipeline specifies the field that will be used for join is ``applications_id_list`` and the result will be put in 
attribute called ``apps`` (`target_field_name`). Besides that, the `target_field` wiil be an array that has a maximum of 128
positions defined by ``max_matches``. The argument ``policy_name`` specifies what policy it will be used for enrichment. 

.. code-block:: python

    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': PORT}],
        timeout = 10000
    )

    pipeline=Pipeline(client=es,
                    name="user-app",
                    pipeline_handler=PipelineHandler(
                        description="enriching user with apps",
                        match_field="applications_id_list",
                        target_field_name="apps",
                        policy_name="apps-json",
                        max_matches=128))

.. py:module:: moredata.enricher.elasticsearch_connector.pipeline_handler

.. autoclass:: Pipeline
    :members:

.. autoclass:: PipelineHandler
    :members:


Policy
------

Policy defines what fields you want to enrich, what is the ``match_field``.

Example
~~~~~~~

Here we are defining a policy for enrich some documents with city. So, all fields inside the list enrich_fields will be part of enrichment result. The ``match_field`` here provides what key will be used for join, and the ``index`` is the document loaded into elasticsearch that has these fields.

.. code-block:: python

    enrich_fields = ["name", "Nome da Grande Região", "Nome da Mesorregião", "Nome da Microrregião", "Nome da Região Rural"]

    policy = Policy(client, name="city-policy", policy_handler=PolicyHandler(type_match="geo_match", 
                                                        index="cities", 
                                                        match_field="geometry", 
                                                        enrich_fields=enrich_fields))


.. py:module:: moredata.enricher.elasticsearch_connector.policy_handler

.. autoclass::Policy
    :members:

.. autoclass:: PolicyHandler
    :members:
