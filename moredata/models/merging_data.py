from geopandas import sjoin
class MergingData:

    def __init__(data_file):
        self.data_file = data_file

    def spatial_join(gdf_enricher ,gdf_enrichering,how, predicate ):
        return sjoin(gdf_enricher, gdf_enrichering,how, predicate)

