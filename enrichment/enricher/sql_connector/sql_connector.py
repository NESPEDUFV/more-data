from ..enricher import IEnricherConnector
import sqlalchemy
import decimal

class SqlConnector(IEnricherConnector):
    def __init__(self, connection_url, table_name, dict_keys, result_attr, column):
        self.engine = sqlalchemy.create_engine(connection_url)
        self.table = sqlalchemy.Table(table_name, sqlalchemy.MetaData(), autoload_with=self.engine)
        self.column = column
        self.dict_keys = dict_keys
        self.result_attr = result_attr

    def _enrich_object(self, obj, table):
        def get_value(obj):
            query = self.table.select().where(self.table.c[self.column] == obj)
            result = self.engine.execute(query)
            
            result_dict = dict(result.first())
            for k, _ in result_dict.items():
                if isinstance(result_dict[k], decimal.Decimal):
                    result_dict[k] = float(result_dict[k])

            return result_dict

        if isinstance(obj, list):
            result_dict = []
            for o in obj:
                result_dict.append(get_value(o))
            return result_dict
        
        return get_value(obj)
            

    def enrich(self, data, **kwargs):
        for d in data.parse(**kwargs):
            objects = d[keys[0]]
            for k in range(1, len(keys)):
                try:
                    objects = objects[k]
                except KeyError as e:
                    return None

            if isinstance(objects, list):
                for obj in objects:
                    d[self.result_attr] = self._enrich_object(obj)         
            else:
                obj[self.result_attr] = self._enrich_object(obj)            

            yield d