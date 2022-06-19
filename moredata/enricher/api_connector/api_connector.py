from ..enricher import IEnricherConnector
from ...models.data import  GeopandasData, JsonData, DaskGeopandas
from ...utils import load_json
import pandas as pd
import dask
from distributed import Client, LocalCluster

class ApiConnector(IEnricherConnector):
    """ApiConnector implements interface IEnricherConnector,
    so this connector can be used to enrich some data.

    Parameters
    ----------
    response_parser: Callable
        a function that will parse the response of the request
        and returns a dict with the values which will enrich the data.

    url_pattern: str
        url_pattern is the route of the api to retrieve values
        which will enrich the data.

    params: Dict
        params are a dict that has key as the variable in route and name is
        where to retrieve the data value to assign in route.

    Attributes
    ----------
    response_parser: Callable

    url_pattern: str

    params: dict
    """

    def __init__(self, response_parser, url_pattern, params):
        self.response_parser = response_parser
        self.url_pattern = url_pattern
        self.params = params

    def _handle_params(cls, pattern, params):
        """
        Replace all variables inside pattern string with params
        values to build the url to request.

        Parameters
        ----------
        pattern: str

        params: Dict

        Returns
        -------
        url: str
        """
        import re

        regex = re.compile("\{.*?\}")
        routes = regex.findall(pattern)

        for route in routes:
            pattern = pattern.replace(route, str(params[route[1 : len(route) - 1]]))

        return pattern

    def _make_request(cls, url, *args, **kwargs):
        """
        Using requests package this method will do the request and return that json.

        Parameters
        ----------
        url: str

        Returns
        -------
        json: Json
        """
        import requests
        from urllib3.exceptions import InsecureRequestWarning

        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        return requests.get(url, verify=False).json()

    def enrichJsonData(self, data, **kwargs):
        responses_cache = {}

        for d in data.parse(**kwargs):
            if self.params["fields"]:
                for field in self.params["fields"]:
                    self.params[field["key"]] = d[field["name"]]

                url = self._handle_params(self.url_pattern, self.params)
                if url in responses_cache.keys():
                    response_value = responses_cache[url]
                else:
                    response_value = self.response_parser(self._make_request(url))
                    responses_cache[url] = response_value

                if response_value is not None:
                    for k, v in response_value.items():
                        d[k] = v

                yield d
                
    # itertuples almost implemented
    # def enrichGeoPandasData1(self, data):
    #     for tuple in data.itertuples():
    #         if self.params["fields"]:
    #             for field in self.params["fields"]:
    #                 self.params[field["key"]] =  getattr(tuple, field["name"])
    #             url = self._handle_params(self.url_pattern, self.params)
    #             data.loc[tuple.Index,'enriched'] = self.response_parser(self._make_request(url))
    #     return data

    def enrichGeoPandasData(self, data):
        for _, row in data.iterrows():
            if self.params["fields"]:

                for field in self.params["fields"]:
                    self.params[field["key"]] = row[field["name"]]
                url = self._handle_params(self.url_pattern, self.params)
                row['enriched'] = self.response_parser(self._make_request(url))
        return data
    def enrich(self, data, **kwargs):
        """Method overrided of interface. This interface do enrichment using
        API as a enricher and return all data enriched as Json. This method
        has a cache that will store as dict the url as key and the response parsed as value
        for don't spend time with requests that are already done previously.

        Parameters
        ----------
        data: Data

        Yields
        ------
        data: Dict
        """

        if isinstance(data, GeopandasData):
            return self.enrichGeoPandasData(data.data)

        elif isinstance(data, DaskGeopandas):
            dask.config.set({"distributed.nanny.environ.MALLOC_TRIM_THRESHOLD_": 0})
            cluster = LocalCluster(n_workers=1, threads_per_worker=2, memory_limit='2GB')
            client = Client(cluster)
            return self.enrichGeoPandasData(data.data).compute()

        elif isinstance(data, JsonData):
            return self.enrichJsonData(data, **kwargs)

 
