from ..enricher import IEnricherConnector
import sqlalchemy
import decimal

class SqlConnector(IEnricherConnector):
    def __init__(self, table_name, dict_keys, result_attr, column, engine=None, connection_url=None):
        if engine is None and connection_url is None:
            raise Exception
        
        if engine is not None:
            self.engine = engine

        if connection_url is not None:
            self.engine = sqlalchemy.create_engine(connection_url)
            #connection?
        
        self.table = sqlalchemy.Table(table_name, sqlalchemy.MetaData(), autoload_with=self.engine)
        self.column = column
        self.dict_keys = dict_keys
        self.result_attr = result_attr

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
            print(obj)
            for o in obj:
                result_dict.append(get_value(o))
            return result_dict
        
        return get_value(obj)
            

    def enrich(self, data, **kwargs):
        for d in data.parse(**kwargs):
            objects = d[self.dict_keys[0]]
            # for k in range(1, len(dict_keys)):
            #     try:
            #         objects = objects[k]
            #     except KeyError as e:
            #         return None

            if isinstance(objects, list):
                if isinstance(objects[0], dict):
                    for obj in objects:
                        obj[self.result_attr] = self._enrich_object(obj)
                else: 
                    d[self.result_attr] = self._enrich_object(objects)             
            else:
                obj[self.result_attr] = self._enrich_object(obj)    

            yield d