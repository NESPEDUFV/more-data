import geopandas
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
    def __init__(self, data_type, data_file):
        self.data_file = data_file
        self.data_type = data_type
        self.enrichers = []

    def add(self, enricher):
        """add enricher in enrichers attribute"""
        self.enrichers.append(enricher)
    
class GeopandasData (Data):

    @classmethod
    def from_geodataframe(self,geodataframe):
        self.data =  geodataframe
        return self

    @classmethod
    def from_path(self, path):
        self.data = geopandas.read_file(path) 
        return self

class JsonData (Data):
    def __init__(self,  parsefunction):
        self.parser = parsefunction
        
    def parse(self, **kwargs):
        """parse calls the parser_func attribute"""
        return self.parser(self.data_file, **kwargs)