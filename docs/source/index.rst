.. enrichment documentation master file, created by
   sphinx-quickstart on Tue Mar 24 19:45:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Enrichment Framework
====================
Its goal is to provide a framework with high extensability for data enrichments

Enricher
----------
Can contains some connectors
:class:`~enrichment.enricher.elasticsearch_connector.elasticsearch_connector`,
:class:`~enrichment.enricher.api_connector.api_connector`. You can choose the enricher appropiately
for your application. 

Elasticsearch
~~~~~~~~~~~~~

If you want to enrich with elasticsearch you have to provide a client to the enricher, 
and others classes 
:class:`~enrichment.enricher.elasticsearch_connector.index_handler`, 
:class:`~enrichment.enricher.elasticsearch_connetor.index_handler.reindex_handler`,
:class:`~enrichment.enricher.elasticsearch_connector.pipeline_handler`,
:class:`~enrichment.enricher.elasticsearch_connector.policy_handler`,
that enricher need.

Firstly, you have to insert your data into elasticsearch, so using ``index_handler``:

.. code-block:: python
   
   
   es = Elasticsearch(
      hosts=[{'host': HOST, 'port': PORT}],
      timeout = 10000
   )

   user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json", unstructured_data=True)
   index_handler = IndexHandler(client, "users", "user")
   index_handler.load_index(parser=data.parse, array_point_field="points_of_interest", geo_location=True, code_h3=True)

Here, you have created a Data with a function that parse your document, that function is a default, but you
can create your own parser function that implements some nice features for your enrichment. After that, you 
instantiate an index_handler and use load_index method, passing a parser and others kwargs. We will enrich a
specific geo_location enrichment so we need the geo_location and code_h3 equals true. The code_h3 is to get the point
and hashing this point using `h3 library <https://github.com/uber/h3>`_. If the lat/long is in array object you have to pass the name of this field.

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

Here we have a geo_location enrichment based on latitude and longitude, and has a query with `CONTAINS`, 
so every point in `points_of_interest` will be enriched if this point is contained by a geo shape that is a field
defined by the policy of city-policy.

.. toctree::
   :maxdepth: 2

   models
   enricher
   elasticsearch_connector
   api_connector


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`