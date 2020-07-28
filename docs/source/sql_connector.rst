.. _sql_connector:

SQL Connector
=============
Examples
~~~~~~~~

This example implements the use of SQL Connector. The example above use mysql as a database and to wok with this RDBMS you don't have to install any other libraries, but if you want to work if SQLite, PostgreSQL you should install the libraries for framework enrich properly without errors. You can see all RDBMS available here: `SQLAlchemy <https://www.sqlalchemy.org/features.html#:~:text=Supported%20Databases,of%20which%20support%20multiple%20DBAPIs.>`_.

You have an option to pass the engine already created instead ``connection_url``. See the especifications on the docstrings of ``SQLConnector`` class.

Besides that, this example use a table named `apps` and a column to query named `#id`, and the result of enrichment is placed on attribute named `apps`. The dict_keys is util to reach at the data that will be used to make the relationship of your original daa and the data stored in database.

.. code-block:: python
    
    # name of file: enrich-sql.py

    URL = "mysql+pymysql://root:root@localhost:3306/database"

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

SQL Connector
-------------

.. py:module:: enrichment.enricher.sql_connector.sql_connector

.. autoclass:: SqlConnector
    :members: