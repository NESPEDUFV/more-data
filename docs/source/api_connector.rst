.. _api_connector:


API Connector
=============
Connector that will enrich data based on API connector. This package uses requests package. 


API Connector
-------------
Examples
~~~~~~~~

This example implements the use of the IBGE API and the conversion between the data entry format and the standard used by the Framework. In the definition of the ``URL_PATTERN`` the parameters that will be used to collect in the API are defined, these ``PARAMETERS`` must be in the standard used by the API. As the Framework works with the JSON format it is necessary to use ``Convert`` to transform the input from CSV to JSON. The Converter takes as a parameter the path to the file to be converted (``CIDADES_DIR_CSV``) and the path of the converted file (``CIDADES_DIR_JSON``).

.. code-block:: python
    
    # name of file: api-ibge.py
    
    from enrichment.enricher import EnricherBuilder, Enricher
    from enrichment.enricher.api_connector import ApiConnector
    from enrichment.models.data import Data
    from enrichment.parser import parse_document
    from enrichment.utils.util import read_json_from_file, Converter


    URL_PATTERN = r'https://servicodados.ibge.gov.br/api/v1/pesquisas/-/indicadores/47001/resultados/{localidade}'

    PARAMETERS = {
      "fields": [
        {
          "key": "localidade",
          "name": "Código da Região Geográfica Imediata"
        }
      ]
    }
     
    Converter.csv_to_json(CIDADES_DIR_CSV, CIDADES_DIR_JSON)
    cidades = Data(data_file=CIDADES_DIR_JSON, parser_func=parse_document, data_type="csv")

    api_ibge_enricher = Enricher(connector=ApiConnector(response_parser=response_parser, url_pattern=URL_PATTERN, params=PARAMETERS))

    cidades_enriched = \
    EnricherBuilder(cidades) \
    .with_enrichment(api_ibge_enricher) \
    .get_result()


Remember to edit the file path (``CIDADES_DIR_CSV`` and ``CIDADES_DIR_JSON``) for the correct behavior and run the example file.

.. code-block:: bash
    
    $ python api-ibge.py
    
.. py:module:: enrichment.enricher.api_connector.api_connector

.. autoclass:: ApiConnector 
    :members:


