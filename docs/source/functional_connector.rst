.. functional_connector:

Functional Connector
====================
Examples
~~~~~~~~
This example implements the use of Functional Region Connector. It uses a simple file extracted from OSM tag called: leisure - fitness_centre that has all fitness centre of a place. Here it counts all fitness centre that is within a raidus around a point of interest specified in ``user_profile_17092019_preprocessed.json`` file.

.. code-block:: python
    
    import os
    import sys
    sys.path.insert(0, os.path.abspath('../../'))

    from enrichment.enricher import EnricherBuilder, Enricher
    from enrichment.models.data import Data
    from enrichment.parser import parse_document
    from enrichment.utils.util import read_json_from_file, Converter
    from enrichment.enricher.osm.functional_region_connector import FunctionalRegionConnector

    DATASETS_DIR = "../../../datasets/"
    FITNESS_CENTRE = DATASETS_DIR + "Locais_OSM/csv/leisure-fitness_centre.csv"

    USER_DATA = DATASETS_DIR + "user_profile_17092019_preprocessed.json"

    if __name__ == "__main__":

        user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json")

        osm_enricher = Enricher(connector=FunctionalRegionConnector(file=FITNESS_CENTRE, radius=500, dict_keys=["points_of_interest"]))

        user_enriched = \
        EnricherBuilder(user) \
        .with_enrichment(osm_enricher) \
        .get_result() 

        import enrichment.utils.util as util

        util.write_json_generator_to_json("../../data/output/osm/functional-fitness-centre", user_enriched, 100000) 

.. code-block:: bash
    
    $ python enrich-osm.py

Functional Region Connector
---------------------------

.. py:module:: enrichment.enricher.osm.functional_region_connector

.. autoclass:: FunctionalRegionConnector
    :members: