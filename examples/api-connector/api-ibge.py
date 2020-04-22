import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from enrichment.enricher import EnricherBuilder, Enricher
from enrichment.enricher.api_connector import ApiConnector
from enrichment.models.data import Data
from enrichment.parser import csv_generator, parse_document
from enrichment.utils.util import read_json_from_file, Converter

DATASETS_DIR = "../../../datasets/"

CIDADES_DIR_CSV = DATASETS_DIR + "cidades_info_polygon.csv"
CIDADES_DIR_JSON = "../../data/output/conversion/cidades_info_polygon.json"

URL_PATTERN = r'https://servicodados.ibge.gov.br/api/v1/pesquisas/-/indicadores/47001/resultados/{localidade}'
PARAMETERS = {
  "fields": [
    {
      "key": "localidade",
      "name": "Código do Município"
    }
  ]
}

if __name__ == "__main__":
  def response_parser(response):
    for res in response:
      for res in res["res"]:
        return {
          "pib_per_capita": res["res"]["2017"]
        }
 
  # Converter.csv_to_json(CIDADES_DIR_CSV, CIDADES_DIR_JSON)
  cidades = Data(data_file=CIDADES_DIR_JSON, parser_func=parse_document, data_type="csv")

  api_ibge_enricher = Enricher(connector=ApiConnector(response_parser=response_parser, url_pattern=URL_PATTERN, params=PARAMETERS))

  cidades_enriched = \
    EnricherBuilder(cidades) \
    .with_enrichment(api_ibge_enricher) \
    .get_result()

  import enrichment.utils.util as util
  util.write_json_generator_to_json("../../data/output/cidades/json/cidades-enriched", cidades_enriched, 1000) 
  util.Converter.json_enriched_to_csv("../../data/output/cidades/json/*.json", "../../data/output/cidades/csv/")
  