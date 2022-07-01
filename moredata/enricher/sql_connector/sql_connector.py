from ..enricher import IEnricherConnector
import sqlalchemy
import decimal
import pandas as pd
from moredata.models.data import GeopandasData, JsonData

class SqlConnector(IEnricherConnector):
    """SQLconnector implements interface IEnricherConnector, so this is a connector that can be used to enrich data.

    Parameters
    ----------
    table_name: str
        name of table that will be used to enrich

    dict_keys: List[str]
        dict_keys is the principal argument to the connector. 
        The connector doesn't know where to get data to make the relationship, 
        so you have to pass the keys or if your data isn't nested, just one key 
        to the connector reach at the the right attribute.

    result_attr: str
        where tha enriched data it supposed to be

    column: str
        name of table column to build the relation.

    engine: :obj:`sqlalchemy.engine.Engine`
        an engine already created by sqlalchemy

    connection_url: str
        the string of connection with host, port, password and database.

    Attributes
    ----------
    table_name: str

    dict_keys: List

    result_attr: str

    column: str

    engine: :obj:`sqlalchemy.engine.Engine`, optional

    connection_url: str, optional
    """

    def __init__(
        self,
        table_name,
        dict_keys,
        result_attr,
        column,
        engine=None,
        connection_url=None,
        df_column = None,
    ):
        if engine is None and connection_url is None:
            raise Exception

        if engine is not None:
            self.engine = engine

        if connection_url is not None:
            self.engine = sqlalchemy.create_engine(connection_url)

        self.table = sqlalchemy.Table(
            table_name, sqlalchemy.MetaData(), autoload_with=self.engine
        )
        self.column = column
        self.dict_keys = dict_keys
        self.result_attr = result_attr
        self.df_column = df_column

    def _enrich_object(self, obj):
        def get_value(obj):
            query = self.table.select().where(self.table.c[self.column] == obj)
            result = self.engine.execute(query)

            first = result.first()

            if first is not None:
                result_dict = dict(first)

                if result_dict is not None:
                    for k, _ in result_dict.items():
                        if isinstance(result_dict[k], decimal.Decimal):
                            result_dict[k] = float(result_dict[k])

                return result_dict
            return None

        if isinstance(obj, list):
            result_dict = []
            for o in obj:
                result_dict.append(get_value(o))
            return result_dict

        return get_value(obj)

    def enrichGeoPandasData(self, data):
        for _,row in data.iterrows():
            row.enriched =self._enrich_object(row[self.df_column])
        return pd.json_normalize(data)

    def enrichJsonData(self, data, **kwargs):
        for d in data.parse(**kwargs):
            objects = d[self.dict_keys[0]]
            for k in range(1, len(self.dict_keys) - 1):
                try:
                    objects = objects[self.dict_keys[k]]
                except KeyError as e:
                    return None

            if isinstance(objects, list):
                if isinstance(objects[0], dict):
                    for obj in objects:
                        obj[self.result_attr] = self._enrich_object(
                            obj[self.dict_keys[-1]]
                        )
                else:
                    d[self.result_attr] = self._enrich_object(objects)
            else:
                d[self.result_attr] = self._enrich_object(objects)

            yield d


    def enrich(self, data, **kwargs):
        """Method overrided of interface. This method do enrichment using RDBMS 
        as a enricher. It walk through the keys to reach at the data that will 
        be used to create the relationship. After, if the object is a list it 
        creates an attribute on parent object, if the object is just a dict it 
        creates an attribute inside.

        Parameters
        ----------
        data: :obj:`Data`
        """

        if isinstance(data, GeopandasData):
            if(self.df_column == None):
                raise Exception('df_column is required in GeopandasData')
            return self.enrichGeoPandasData(data.data)

        elif isinstance(data, JsonData):
            return self.enrichJsonData(data, **kwargs)

 