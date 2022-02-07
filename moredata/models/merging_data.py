import geopandas
class MergingData:

    @classmethod
    def from_geodataframe(self,geodataframe):
        self.data = geopandas.read_file(geopandas.datasets.get_path(geodataframe))
        return self.data

    @classmethod
    def from_path(self, path):
        self.data = geopandas.read_file(path) 
        return self.data

    @classmethod
    def spatial_join(self, gdf_enricher ,gdf_enrichering,how, predicate ):
        self.data = geopandas.sjoin(gdf_enricher, gdf_enrichering,how, predicate)
        return self.data