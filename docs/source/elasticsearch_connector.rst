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

.. py:module:: enrichment.enricher.elasticsearch_connector.pipeline_handler

.. autoclass:: Pipeline
    :members:


PipelineHandler
---------------

.. autoclass:: PipelineHandler
    :members:


Policy
------

.. py:module:: enrichment.enricher.elasticsearch_connector.policy_handler

.. autoclass::Policy
    :members:


PolicyHandler
-------------

.. autoclass:: PolicyHandler
    :members: