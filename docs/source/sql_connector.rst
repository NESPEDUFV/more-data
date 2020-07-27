.. _sql_connector:

SQL Connector
=============

SQL Connector
-------------
Examples
~~~~~~~~

This example enrich implements the use of SQL Connector...

..code-block:: python
    
    # name of file: enrich-sql.py

    from enrichment.enricher import EnricherBuilder, Enricher
    from enrichment.enricher.sql_connector import SqlConnector
    from enrichment.models.data import Data
    from enrichment.parser import parse_document
    from enrichment.utils.util import read_json_from_file, Converter

    user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json")

    sql_enricher = Enricher(connector=SqlConnector(connection_url=URL, table_name="apps", column='#id', result_attr="apps", dict_keys=["applications_id_list"]))

    user_enriched = \
	  EnricherBuilder(user) \
	  .with_enrichment(sql_enricher) \
	  .get_result() 

    import enrichment.utils.util as util

    util.write_json_generator_to_json("../../data/output/sql/test", user_enriched, 100000) 

.. code-block:: bash
    
    $ python enrich-sql.py

.. py:module:: enrichment.enricher.sql_connector.sql_connector

.. autoclass:: SqlConnector
    :members: