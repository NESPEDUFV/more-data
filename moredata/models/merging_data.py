import geopandas
class MergingData:

    @classmethod
    def from_geodataframe(self,geodataframe):
        self.data = geopandas.datasets.get_path(geodataframe)
        return self

    @classmethod
    def from_path(self, path):
        self.data = geopandas.read_csv(path) 
        return self

    def spatial_join(self, gdf_enricher ,gdf_enrichering,how, predicate ):
        return geopandas.sjoin(gdf_enricher, gdf_enrichering,how, predicate)