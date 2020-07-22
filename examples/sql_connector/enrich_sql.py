import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

from enrichment.enricher import EnricherBuilder, Enricher
from enrichment.enricher.sql_connector import SqlConnector
from enrichment.models.data import Data
from enrichment.parser import parse_document
from enrichment.utils.util import read_json_from_file, Converter

DATASETS_DIR = "../../../datasets/"
USER_DATA = "../../../datasets/user_profile_17092019_preprocessed_reducted.json"

URL = "mysql+pymysql://root:root@localhost:3306/nesped"

if __name__ == "__main__":
    user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json")

    sql_enricher = Enricher(connector=SqlConnector(connection_url=URL, table_name="apps", column='#id', result_attr="apps", dict_keys=["applications_id_list"]))

    user_enriched = \
	  EnricherBuilder(user) \
	  .with_enrichment(sql_enricher) \
	  .get_result() 

    import enrichment.utils.util as util

    util.write_json_generator_to_json("../../data/output/sql/test", user_enriched, 100000) 
    
    