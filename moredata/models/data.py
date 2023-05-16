import geopandas
import dask_geopandas


class Data:
    """Data object represents a file like csv, json
    with a function to parser that file.

    Parameters
    ----------
    parser_func: function
    data_type: str
        type of data, the extension of file.
    data_file: str
        where the data is.


    Attributes
    ----------

    parser_func: function

    data_type: str

    data_file: str

    enrichers: array
        array of enrichers.
    """

    def __init__(self):
        self.enrichers = []

    def add(self, enricher):
        """add enricher in enrichers attribute"""
        self.enrichers.append(enricher)


class GeopandasData(Data):
    def __init__(self, data):
        super().__init__()
        self.data = data

    @classmethod
    def from_geodataframe(cls, geodataframe):
        return GeopandasData(geodataframe)

    @classmethod
    def from_path(cls, path):
        return GeopandasData(geopandas.read_file(path))


class DaskGeopandasData(Data):
    def __init__(self, data):
        super().__init__()
        self.data = data

    @classmethod
    def from_geodataframe(cls, geodataframe, npartitions=4):
        return DaskGeopandasData(
            dask_geopandas.from_geopandas(geodataframe, npartitions)
        )

    @classmethod
    def from_dask_geodataframe(cls, dask_geodataframe):
        return DaskGeopandasData(dask_geodataframe)

    @classmethod
    def from_path(cls, path, npartitions=4):
        return DaskGeopandasData(dask_geopandas.read_file(path, npartitions))


class JsonData(Data):
    def __init__(self, data_file, parser):
        self.data_file = data_file
        self.parser = parser

    def parse(self, **kwargs):
        """parse calls the parser_func attribute"""
        return self.parser(self.data_file, **kwargs)
