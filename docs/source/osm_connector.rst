.. _osm_connector:

OSM Connector
=============


OSM Connector
-------------
Examples
~~~~~~~~

This example enrich implements the use of OSM Connector...

..code-block:: python
    
    # name of file: enrich-osm.py

    from enrichment.enricher import EnricherBuilder, Enricher
    from enrichment.enricher.osm_connector import OSMConnector
    from enrichment.models.data import Data
    from enrichment.parser import parse_document
    from enrichment.utils.util import read_json_from_file, Converter

    user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json")

    osm_enricher = Enricher(connector=OSMConnector(key="amenity", value="hospital", place_name="São Paulo", radius=100, dict_keys=["points_of_interest"]))

    user_enriched = \
	  EnricherBuilder(user) \
	  .with_enrichment(osm_enricher) \
	  .get_result() 

    import enrichment.utils.util as util

    util.write_json_generator_to_json("../../data/output/osm/amenity-cafe-mg", user_enriched, 100000) 

.. code-block:: bash
    
    $ python enrich-osm.py

.. py:module:: enrichment.enricher.osm_connector.osm_connector

.. autoclass:: OSMConnector
    :members: