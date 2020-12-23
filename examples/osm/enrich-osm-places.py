import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

from enrichment.enricher import EnricherBuilder, Enricher
from enrichment.enricher.osm.osm_places_connector import OSMPlacesConnector 
from enrichment.models.data import Data
from enrichment.parser import parse_document
from enrichment.utils.util import read_json_from_file, Converter

DATASETS_DIR = "../../../datasets/"
FITNESS_CENTRE = DATASETS_DIR + "Locais_OSM/csv/leisure-fitness_centre.csv"

GAS_STATIOSN_DATA_JSON = "/home/gegen07/dev/nesped/profrotas/datasets/postos/postos_brasil_classificados.json"

if __name__ == "__main__":

    gas_stations = Data(data_file=GAS_STATIOSN_DATA_JSON, parser_func=parse_document, data_type="json")

    osm_enricher = Enricher(connector=OSMPlacesConnector(key="amenity", value="fuel", geometry_intersected=True, radius=10))
    gas_stations_enriched = osm_enricher.enrich(data=gas_stations)

    import enrichment.utils.util as util

    util.write_json_generator_to_json("/home/gegen07/dev/nesped/profrotas/datasets/postos/postos_brasil_classificados_polygons", gas_stations_enriched, 100000) 