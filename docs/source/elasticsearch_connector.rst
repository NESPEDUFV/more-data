.. _elasticsearch_connector:


Elasticsearch Connector
=======================


Elasticsearch Connector
-----------------------

.. py:module:: enrichment.enricher.elasticsearch_connector.elasticsearch_connector

.. autoclass:: ElasticsearchConnector 
    :members:


Index Handler
-------------

.. py:module:: enrichment.enricher.elasticsearch_connector.index_handler

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

.. py:module:: enrichment.enricher.elasticsearch_connector.pipeline_handler

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


.. py:module:: enrichment.enricher.elasticsearch_connector.policy_handler

.. autoclass::Policy
    :members:

.. autoclass:: PolicyHandler
    :members:
