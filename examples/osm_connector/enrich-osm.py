import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

from enrichment.enricher import EnricherBuilder, Enricher
from enrichment.enricher.osm_connector import OSMConnector
from enrichment.models.data import Data
from enrichment.parser import parse_document
from enrichment.utils.util import read_json_from_file, Converter

DATASETS_DIR = "../../../datasets/"
HOSPITAL_DIR = DATASETS_DIR + "Locais_OSM/csv/amenity_hospital.csv"

USER_DATA = "../../../datasets/user_profile_17092019_preprocessed.json"

if __name__ == "__main__":
    
    user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json")

    osm_enricher = Enricher(connector=OSMConnector(file=HOSPITAL_DIR, radius=100))

    user_enriched = \
	  EnricherBuilder(user) \
	  .with_enrichment(osm_enricher) \
	  .get_result(keys=["points_of_interest"]) 

    import enrichment.utils.util as util
    util.write_json_generator_to_json("../../data/output/osm/user-enriched", user_enriched, 100000) 